import vtk
import numpy as np
import helpfunction as pty

l2n = lambda l: np.array(l)
n2l = lambda n: list(n)
ren = vtk.vtkRenderer()


def isHit_transducer_skull(skull_obbTree, transducer_obbTree):
    code  = skull_obbTree.IntersectWithOBBTree(transducer_obbTree)
    if code ==0:
        return False
    return True

def isHit(obbTree, pSource, pTarget):

    code =obbTree.IntersectWithLine(pSource,pTarget, None, None)
    if code ==0:
        return False
    return True

def GetIntersect(obbTree, pSource, pTarget):

    # vtk place holder for points cell_id
    points = vtk.vtkPoints()
    cellIds = vtk.vtkIdList()

    # find intersection point of skull (from skull obbtree)
    # this def is little bit weird (input,input,output,output)
    code = obbTree.IntersectWithLine(pSource, pTarget, points, cellIds)


    pointData = points.GetData()
    noPoints = pointData.GetNumberOfTuples()
    nolds = cellIds.GetNumberOfIds()

    assert (noPoints == nolds)

    pointsInter = []
    cellIdsInter = []

    # idx is number of intersection point per one ray
    for idx in range(noPoints):
        pointsInter.append(pointData.GetTuple3(idx))
        cellIdsInter.append(cellIds.GetId(idx))


    return pointsInter ,cellIdsInter

def calVecRefraction(enter_vector, normal_skull, n1, n2):

    # this def calculate angle between two vectors
    # return refraction vector and tilted angle
    S1_b = l2n(enter_vector)
    N_b = l2n(normal_skull)

    S1 = S1_b / np.linalg.norm(S1_b)
    N =N_b/np.linalg.norm(N_b)

    n = n1/n2

    crossP = np.dot(N,S1)
    crossN = np.cross(-N,S1)
    A = n * (np.cross(N, crossN))
    B =(1-(n**2)*crossP*crossP)
    T = (1 - (n ** 2) * (1 - np.dot(S1, N) ** 2))
    dummy = np.zeros((1, 3))

    angle = np.arccos(np.dot(S1_b,N_b)/(np.linalg.norm(S1_b)*np.linalg.norm(N_b)))

    if T>0:
        #S2 = (A-N*np.sqrt(B))
        S2 = n * (S1 + N * np.dot(S1, -N)) - N * np.sqrt(1 - (n ** 2) * (1 - np.dot(S1, N) ** 2))
    else:
        S2 =  dummy   ######( outside of critical angle)



    return S2, angle

def reflection_coefficient(angle, up_properties, down_properties):

    up_density = up_properties[0]
    down_density = down_properties[0]

    up_speed = up_properties[1]
    down_speed = down_properties[1]
    theta = np.radians(angle)

    m = down_density / up_density
    n = up_speed / down_speed

    # test for critical angle
    test = (1 - ((np.sin(theta) * np.sin(theta)) / (n * n)))
    test[np.nonzero(test<0)[0]] = 0

    b = m * np.cos(theta);
    c = n * np.sqrt(test);
    Reflection = abs((b - c)/ (b + c));

    return Reflection

def calculator (skull_cut,focus,transducer,target,raycasting_length, skull_properties, water_properties,random_properties):

    # define physical property
    skull_speed  = skull_properties[1]
    water_speed  = water_properties[1]
    random_speed = random_properties[1]

    # vtk dataform for normal and vector calculation
    obbSkull = vtk.vtkOBBTree()
    obbSkull.SetDataSet(skull_cut)
    obbSkull.BuildLocator()

    obbFocus = vtk.vtkOBBTree()
    obbFocus.SetDataSet(focus.GetOutput())
    obbFocus.BuildLocator()

    # get normal
    normalsCalcSkull = vtk.vtkPolyDataNormals()
    normalsCalcSkull.SetInputData(skull_cut)

    # define normals direction outside of skull center
    normalsCalcSkull.ComputePointNormalsOff()
    normalsCalcSkull.ComputeCellNormalsOn()
    normalsCalcSkull.SplittingOff()
    normalsCalcSkull.FlipNormalsOff()
    normalsCalcSkull.AutoOrientNormalsOff()
    normalsCalcSkull.Update()

    normalsSkull = normalsCalcSkull.GetOutput().GetCellData().GetNormals()


    # set vtk place holder
    out_intersection_point = np.zeros((transducer.GetNumberOfPoints(), 3))
    in_intersection_point  = np.zeros((transducer.GetNumberOfPoints(), 3))
    second_beam_end        = np.zeros((transducer.GetNumberOfPoints(), 3))
    final_beam_end         = np.zeros((transducer.GetNumberOfPoints(), 3))
    result_2layer          = np.zeros((transducer.GetNumberOfPoints(), 1))
    result_1layer          = np.zeros((transducer.GetNumberOfPoints(), 1))

    dummy_points_in    = vtk.vtkPoints()
    dummy_polydata_in  = vtk.vtkPolyData()
    dummy_vectors_in   = vtk.vtkDoubleArray()
    dummy_vectors_in.SetNumberOfComponents(3)


    dummy_points_out    = vtk.vtkPoints()
    dummy_polydata_out  = vtk.vtkPolyData()
    dummy_vectors_out   = vtk.vtkDoubleArray()
    dummy_vectors_out.SetNumberOfComponents(3)


    angle_outskull  = np.zeros((transducer.GetNumberOfPoints(),1))
    angle_inskull   = np.zeros((transducer.GetNumberOfPoints(),1))

    ################################################################################################################################
    # iterate as number of beam lines
    ################################################################################################################################
    for idx in range(transducer.GetNumberOfPoints()):
        point_transducer = transducer.GetPoint(idx)



        ################################################################################################################################
        # (Out skull surface) check whether intersect or not between skull_out and beam line
        ################################################################################################################################
        if isHit(obbSkull,point_transducer,target):

            # find intersection point transducer to skull (skull_out surface)
            outskull_inter_point, outskull_inter_cellid = GetIntersect(obbSkull, point_transducer, target)
            # save first intersection point
            out_intersection_point[idx][:] = l2n(outskull_inter_point[0])

            # find normal at intersection point
            normalSkull_out = normalsSkull.GetTuple(outskull_inter_cellid[0])
            # calculate vector first beam line
            outskull_enter_vector = n2l(l2n(target)-l2n(point_transducer))


            # calculate refraction vector and refraction angle at outskull surface
            S2, angle_outskull[idx] = calVecRefraction(outskull_enter_vector, normalSkull_out, skull_speed, random_speed)


            dummy_points_out.InsertNextPoint(outskull_inter_point[0])
            dummy_vectors_out.InsertNextTuple(normalSkull_out)

            ################################################################################################################################
            # check beam line can penetrate skull_out (from critical angle)
            # if S2 == 0 this beam line has refraction angle which is greater than critical angle
            ################################################################################################################################
            if np.any(S2 != 0):

                # make second beam line (skull_out to skull_in)
                refraction_vector = n2l(S2)
                refract_beam_start = n2l(l2n(outskull_inter_point[0]) + 0.1 * l2n(refraction_vector))
                # calculate second beam line end (length is user setting value)
                refract_beam_end = n2l(l2n(outskull_inter_point[0]) + raycasting_length * l2n(refraction_vector))

                second_beam_end[idx][:] = refract_beam_end



                if isHit(obbFocus, outskull_inter_point[0], refract_beam_end):
                    result_1layer[idx] = 1

                ################################################################################################################################
                # (In skull surface) check whether intersect or not between skull_in and beam line
                ################################################################################################################################
                if isHit(obbSkull, refract_beam_start, refract_beam_end):

                    # find intersection point skull_out to skull_in
                    inskull_inter_point, inskull_inter_cellid = GetIntersect(obbSkull, refract_beam_start, refract_beam_end)

                    # there are some artifacts at inside of the skull
                    # thus, it will be select several point as intersection point
                    # So we have to choose last row (under in end )
                    end = len(l2n(inskull_inter_point))-1

                    in_intersection_point[idx][:] = l2n(inskull_inter_point[end])

                    # find normal of skull_in second beam line
                    normalSkull_in = normalsSkull.GetTuple(inskull_inter_cellid[end])
                    # calculate refraction vector at inskull surface to brain region
                    S2_in,  angle_inskull[idx] = calVecRefraction(refraction_vector, -l2n(normalSkull_in), water_speed, skull_speed)


                    # for plotting
                    normalSkull_in_plot = -l2n(normalSkull_in)
                    dummy_points_in.InsertNextPoint(inskull_inter_point[end])
                    dummy_vectors_in.InsertNextTuple(normalSkull_in_plot)



                    ################################################################################################################################
                    # check beam line can penetrate skull_in (from critical angle)
                    # if S2 == 0 this beam line has refraction angle which is greater than critical angle
                    ################################################################################################################################
                    if np.any(S2_in != 0):
                        refraction_vector_in = n2l(S2_in)
                        f_beam_end = (l2n(inskull_inter_point[end]) + raycasting_length * (l2n(refraction_vector_in)))

                        # checking the computational error
                        if f_beam_end[2]< outskull_inter_point[0][2]:
                            final_beam_end[idx][:] =f_beam_end

                            if isHit(obbFocus,  inskull_inter_point[end], f_beam_end):
                                result_2layer[idx] = 1


                    # out skull surface normal for plotting

                    dummy_polydata_out.SetPoints(dummy_points_out)
                    dummy_polydata_out.GetPointData().SetNormals(dummy_vectors_out)
                    arrow = vtk.vtkArrowSource()

                    glyphEarth_out = vtk.vtkGlyph3D()
                    glyphEarth_out.SetInputData(dummy_polydata_out)
                    glyphEarth_out.SetSourceConnection(arrow.GetOutputPort())
                    glyphEarth_out.SetVectorModeToUseNormal()
                    glyphEarth_out.SetScaleFactor(5)

                    glyphMapperEarth_out = vtk.vtkPolyDataMapper()
                    glyphMapperEarth_out.SetInputConnection(glyphEarth_out.GetOutputPort())

                    glyphActorEarth_out = vtk.vtkActor()
                    glyphActorEarth_out.SetMapper(glyphMapperEarth_out)
                    glyphActorEarth_out.GetProperty().SetColor([1,0,0])




                    # in skull surface normal for plotting
                    dummy_polydata_in.SetPoints(dummy_points_in)
                    dummy_polydata_in.GetPointData().SetNormals(dummy_vectors_in)
                    arrow = vtk.vtkArrowSource()

                    glyphEarth_in = vtk.vtkGlyph3D()
                    glyphEarth_in.SetInputData(dummy_polydata_in)
                    glyphEarth_in.SetSourceConnection(arrow.GetOutputPort())
                    glyphEarth_in.SetVectorModeToUseNormal()
                    glyphEarth_in.SetScaleFactor(5)

                    glyphMapperEarth_in = vtk.vtkPolyDataMapper()
                    glyphMapperEarth_in.SetInputConnection(glyphEarth_in.GetOutputPort())

                    glyphActorEarth_in = vtk.vtkActor()
                    glyphActorEarth_in.SetMapper(glyphMapperEarth_in)
                    glyphActorEarth_in.GetProperty().SetColor([1,0,1])


    # incidence angle out skull surface(degree)
    angle_outskull = 180 - np.degrees(angle_outskull)
    # incidence angle in skull surface(degree)
    angle_inskull  = 180 - np.degrees(angle_inskull)


    # calculate reflection coefficient
    Out_RC = reflection_coefficient(angle_outskull, random_properties, skull_properties)
    Out_RC[Out_RC > 1] = 1

    In_RC = reflection_coefficient(angle_inskull, skull_properties, water_properties)
    In_RC[In_RC > 1] = 1


    Out_ARC = np.mean(Out_RC)
    In_ARC = np.mean(In_RC)

    ARC = (Out_ARC+In_ARC)/2



    return out_intersection_point,in_intersection_point,final_beam_end,second_beam_end,result_2layer,result_1layer,ARC, Out_ARC  ,glyphActorEarth_out, glyphActorEarth_in


