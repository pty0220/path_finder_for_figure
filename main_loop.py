import numpy as np
import vtk
import datetime
import time
import multiprocessing

import tkinter.filedialog as tk
import os


from   tqdm         import *
from   brain_target import *  ## developer made help function
from F_interactorstyle import FStyle


import calculator as cal    ## developer made help function
import helpfunction as pty  ## developer made help function

l2n = lambda l: np.array(l)
n2l = lambda n: list(n)


"""""
##########################################################################################################################################################
##########################################################################################################################################################
Running for calculation and plotting
##########################################################################################################################################################
##########################################################################################################################################################
"""""




def loop(number_of_trandcuer,length_transducer2target,range_angle,centerline_vector,Target,spherePoly, ROC, width,frist_cutskull
         ,focus,raycasting_length,skull_properties,water_properties,random_properties, startTime,Target_name,number_of_beamlines,beamline_mesh_mean
         ,focal_length, skull_file_name,transducer_plot,iren):
    # place holder for vtk files
    transducer             = {}
    transducer_actor       = {}
    out_intersection_point = {}
    in_intersection_point  = {}
    final_beam_end         = {}
    layer1_beam_end        = {}
    result                 = {}
    result_layer1          = {}
    ARC                    = {}
    ARC_layer1             = {}
    T_plot                 = {}
    T_plot_actor           = {}

    ren = iren.GetRenderWindow().GetRenderers().GetFirstRenderer()


    for jj in range(1):
        step = 0  # -10+5*jj

        ### make analysis area as vtk data (computational range)
        a_range, a_range_actor, transducer_mesh_mean, transducer_mesh_dis \
            = pty.make_analysis_rage2(number_of_trandcuer,
                                      length_transducer2target + step,range_angle, 0.2,
                                      centerline_vector, Target)

        number_position = a_range.GetNumberOfPoints()
        print("#")
        print("#")
        print("#")
        print("#")
        print("#")
        print("Step size of transducer is: "+str(transducer_mesh_mean)+" mm")
        val = 'y'#input("If you want to start calculate type 'y' : ")

        if val == 'y':
            ### get number of point of transducer center (from computational range)


            ### make numpy place holder
            percentage        = np.zeros((number_position, 7))
            percentage_layer1 = np.zeros((number_position, 7))
            ARC_result        = np.zeros((number_position, 7))
            ARC_layer1_result = np.zeros((number_position, 7))



            # print(" ")
            # print("Start calcule reflection coefficient at each transducer")
            ################################################################################################################
            ################################################################################################################
            ############## Main Calculation !!!!!!!!!
            ################################################################################################################
            ################################################################################################################
            for i in tqdm(range(number_position)):  # calculate vector of analysis range

                # get transducer center point from computational range
                top_point = a_range.GetPoint(i)

                # get vector between transducer and target
                vector = l2n(top_point) - l2n(Target)
                dir_vector = (vector / np.linalg.norm(vector))




                # make transducer as vtk data
                transducer['tran' + str(i)], transducer_actor['tran_actor' + str(i)], xy_angle, z_angle\
                    = pty.make_transducer(spherePoly, ROC, width, length_transducer2target + step, dir_vector, Target, 1, [0.5, 0.5, 0.5])

                # stl file for just plot
                T_plot['tran' + str(i)], T_plot_actor['tran_actor' + str(i)], xy_angle, z_angle = \
                    pty.make_transducer(transducer_plot, ROC, width, length_transducer2target, dir_vector, Target, 1,[0.7, 0.7, 0.8])

                if i>0:
                    ren.RemoveActor(T_plot_actor['tran_actor' + str(i-1)])
                    iren.GetRenderWindow().Render()
                ren.AddActor(T_plot_actor['tran_actor' + str(i)])
                iren.GetRenderWindow().Render()


                skull_cut, skull_cut_actor = pty.cut_skull_loop(frist_cutskull, Target, dir_vector)

                if i > 0:
                    ren.RemoveActor(skull_cut_actor)
                    iren.GetRenderWindow().Render()
                ren.AddActor(skull_cut_actor)
                iren.GetRenderWindow().Render()

                intersectionPolyFilter = vtk.vtkIntersectionPolyDataFilter()
                intersectionPolyFilter.SetInputData(0, frist_cutskull)
                intersectionPolyFilter.SetInputData(1, transducer['tran' + str(i)])
                intersectionPolyFilter.Update()
                test_intersection = intersectionPolyFilter.GetOutput()



                if test_intersection.GetNumberOfPoints() == 0:
                #if a == 0:
                    # cut skull for speed

                    # find intersection point at each beam lines with skull
                    out_intersection_point[str(i)], in_intersection_point[str(i)], final_beam_end[str(i)], layer1_beam_end[str(i)], result[str(i)],result_layer1[str(i)], ARC[str(i)], ARC_layer1[str(i)], glyphActorEarth_out,glyphActorEarth_out_in\
                        = cal.calculator(skull_cut, focus, transducer['tran' + str(i)], Target, raycasting_length, skull_properties, water_properties, random_properties)

                    firstline_actor = {}
                    secondline_actor = {}
                    finalline_actor = {}

                    # for plotting beam lines (first, second and final)
                    # iterate as number of beam lines
                    for idx in range(number_of_beamlines):

                        # draw line transducer to out skull surface
                        if np.any(out_intersection_point[str(i)][idx][:] != 0):

                            firstline, firstline_actor[str(idx)] = \
                                pty.addLine(ren,  transducer['tran' + str(i)].GetPoint(idx), n2l(out_intersection_point[str(i)][idx][:]), [1, 1, 0])

                            # if you want to draw first beam, draw (add vtk render)


                            # draw line out skull surface to in skull surface
                            if np.any(in_intersection_point[str(i)][idx][:] != 0):
                                secondline, secondline_actor[str(idx)] = \
                                    pty.addLine(ren, n2l(out_intersection_point[str(i)][idx][:]),
                                                n2l(in_intersection_point[str(i)][idx][:]), [0, 0, 1])

                                layer1_finish, layer1_finish_actor = \
                                    pty.addLine(ren, n2l(out_intersection_point[str(i)][idx][:]), n2l(layer1_beam_end[str(i)][idx][:]),
                                                [0, 0.5, 1])

                                # if you want to draw second beam, draw (add vtk render)

                                if np.any(final_beam_end[str(i)][idx][:] != 0):
                                    finalline, finalline_actor[str(idx)] = pty.addLine(ren,
                                                                                       n2l(in_intersection_point[str(i)][idx][:]),
                                                                                       n2l(final_beam_end[str(i)][idx][:]),
                                                                                       [1, 0.5, 0])

                    for h in range(len(firstline_actor)):
                        ren.AddActor(firstline_actor[str(h)])
                    iren.GetRenderWindow().Render()

                    for h in range(len(secondline_actor)):
                        ren.AddActor(list(secondline_actor.values())[h])
                    iren.GetRenderWindow().Render()

                    for h in range(len(finalline_actor)):
                        ren.AddActor(list(finalline_actor.values())[h])
                    iren.GetRenderWindow().Render()

                    for h in range(len(firstline_actor)):
                        ren.RemoveActor(firstline_actor[str(h)])

                    for h in range(len(secondline_actor)):
                        ren.RemoveActor(list(secondline_actor.values())[h])

                    for h in range(len(finalline_actor)):
                        ren.RemoveActor(list(finalline_actor.values())[h])
                    iren.GetRenderWindow().Render()




                # ray tracking result

                    percentage[i][0] = (np.sum(result[str(i)]) / transducer['tran' + str(i)].GetNumberOfPoints()) * 100
                    percentage[i][1] = i
                    percentage[i][2] = xy_angle
                    percentage[i][3] = z_angle
                    percentage[i][4:] = l2n(top_point)

                    percentage_layer1[i][0] = (np.sum(result_layer1[str(i)]) / transducer['tran' + str(i)].GetNumberOfPoints()) * 100
                    percentage_layer1[i][1] = i
                    percentage_layer1[i][2] = xy_angle
                    percentage_layer1[i][3] = z_angle
                    percentage_layer1[i][4:] = l2n(top_point)

                    # ARC result
                    ARC_result[i][0] = ARC[str(i)]
                    ARC_result[i][1] = i
                    ARC_result[i][2] = xy_angle
                    ARC_result[i][3] = z_angle
                    ARC_result[i][4:] = l2n(top_point)

                    # ARC layer1 result
                    ARC_layer1_result[i][0] = ARC_layer1[str(i)]
                    ARC_layer1_result[i][1] = i
                    ARC_layer1_result[i][2] = xy_angle
                    ARC_layer1_result[i][3] = z_angle
                    ARC_layer1_result[i][4:] = l2n(top_point)


                else:
                    percentage[i][0] = 0
                    percentage[i][1] = i
                    percentage[i][2] = xy_angle
                    percentage[i][3] = z_angle
                    percentage[i][4:] = l2n(top_point)

                    percentage[i][0] = 0
                    percentage[i][1] = i
                    percentage[i][2] = xy_angle
                    percentage[i][3] = z_angle
                    percentage[i][4:] = l2n(top_point)


                    ARC_result[i][0] = 1
                    ARC_result[i][1] = i
                    ARC_result[i][2] = xy_angle
                    ARC_result[i][3] = z_angle
                    ARC_result[i][4:] = l2n(top_point)

                    ARC_layer1_result[i][0] = 1
                    ARC_layer1_result[i][1] = i
                    ARC_layer1_result[i][2] = xy_angle
                    ARC_layer1_result[i][3] = z_angle
                    ARC_layer1_result[i][4:] = l2n(top_point)

            ################################################################################################################
            ################################################################################################################
            ############## Main Calculation !!!!!!!!!
            ################################################################################################################
            ################################################################################################################







            possible_position = number_position - np.sum(ARC_result[:,0] == 1)



            # sorting result as ray casting percentage increase
            result_percentage = sorted(percentage, key=lambda percentage: percentage[0], reverse=True)
            maximum_percentage = max(percentage[:, 0])

            # sorting result as ray casting percentage increase
            result_layer1_percentage = sorted(percentage_layer1, key=lambda percentage: percentage[0], reverse=True)
            maximum_percentage = max(percentage[:, 0])

            # sorting result as ARC increase
            result_ARC = sorted(ARC_result, key=lambda ARC_result: ARC_result[0])
            minimum_ARC = min(ARC_result[:, 0])

            # sorting result as ARC layer1 increase
            layer1_result_ARC = sorted(ARC_layer1_result, key=lambda ARC_layer1_result: ARC_layer1_result[0])



            # made time when this file made it
            now = datetime.datetime.now()
            now_data_time = now.strftime('%Y-%m-%d %H_%M')
            endTime = time.time() - startTime

            # information about calculation to write in header
            header = '{0:^5s}\n{1:^5s} \n{2:^5s} \n{3:^5s}\n{4:^5s}\n{5:^5s}\n{6:^5s}\n{7:^5s}\n{8:^5s}\n{9:^5s}\n{10:^5s}\n{11:^5s}'\
                .format('This file made at: '+str(now_data_time),
                        'Target: '+str(Target_name)+',  coordinate: '+str(Target),
                        'Number of possible transducer position: ' + str(possible_position) + ',  Whole transducer position(involve invalidate): ' + str(number_position),
                        'Distance between Transducer: ' + str(transducer_mesh_mean)+' mm',
                        'Number of beam lines '+str(number_of_beamlines),
                        'Distance between beam lines: '+str(beamline_mesh_mean)+' mm',
                        'ROC: '+str(ROC)+',  width: '+str(width)+',  focal length: '+str(focal_length),
                        'Skull STL file: '+str(skull_file_name),
                        'calculation time '+str(endTime),
                        'column means: (1)ARC/percentage, (2)position number, (3)xy_angle, (4)z_angle, (5)x, (6)y, (7)z',
                        '',
                        '')

            # make folder
            make_folder_name = Target_name + ' result beam_line'+ str(number_of_beamlines) + ' loaction'+ str(number_position)+"  " + str(now_data_time)
            os.mkdir(make_folder_name)

            # adjust path for saving txt
            now_dir  = os.getcwd()
            os.chdir(now_dir+'\\'+make_folder_name)

            np.savetxt(Target_name + " tracking result & step " + str(step) + 'mm  '+ str(now_data_time), result_percentage , '%5.20f',header = header )
            np.savetxt(Target_name + " one layer tracking result & step " + str(step) + 'mm  ' + str(now_data_time),result_layer1_percentage, '%5.20f', header=header)
            np.savetxt(Target_name + " ARC result & step "      + str(step) + 'mm  '+ str(now_data_time), result_ARC        , '%5.20f',header = header)
            np.savetxt(Target_name + " one layer skull ARC result & step "      + str(step) + 'mm  ' + str(now_data_time), layer1_result_ARC, '%5.20f',  header=header)



            print("###########################################################################")
            print("This is calculation version ###############################################")
            print("###########################################################################")
            print("")
            print("The target is "+Target_name)
            print("Number of possible transducer position is " + str(possible_position))
            print("Distance between transducer: " +str(transducer_mesh_mean))
            print("Number of beam lines is " + str(transducer['tran' + str(1)].GetNumberOfPoints()))
            print("Distance between beam lines: " + str(beamline_mesh_mean))
            print("")
            print("Maximum accuracy of this transducer's position is " + str(maximum_percentage) + "%")
            print("Minimum reflection coefficient is " + str(minimum_ARC))
            print("")
            print("(from ARC result) The optimal position of transducer location is " + str(ARC_result[i][4:]))
            print("")
            print("Running time is " + str(endTime))
