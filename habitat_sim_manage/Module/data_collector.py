import os
import cv2
import shutil
import numpy as np
from copy import deepcopy
from getch import getch
from scipy.spatial.transform import Rotation as R


from habitat_sim_manage.Config.config import SIM_SETTING
from habitat_sim_manage.Module.sim_manager import SimManager

class DataCollector(SimManager):
    def __init__(self, glb_file_path=None, control_mode=None, save_dataset_folder_path=None):
        super().__init__()

        self.save_dataset_folder_path = None
        self.image_folder_path = None
        self.sparse_folder_path = None
        self.image_pose_file = None
        self.image_idx = 1

        if glb_file_path is not None:
            assert self.loadSettings(glb_file_path)

        if control_mode is not None:
            assert self.setControlMode(control_mode)

        if save_dataset_folder_path is not None:
            assert self.createDataset(save_dataset_folder_path)
        return

    def reset(self):
        super().reset()
        self.save_dataset_folder_path = None
        self.image_folder_path = None
        self.sparse_folder_path = None
        self.image_pose_file = None
        self.image_idx = 1
        return True

    def saveSceneInfo(self):
        hfov = None
        for sensor in self.sim_loader.cfg.agents[0].sensor_specifications:
            if sensor.uuid == 'color_sensor':
                hfov = float(self.sim_loader.cfg.agents[0].sensor_specifications[0].hfov) * np.pi / 180.
                break

        if hfov is None:
            print('[ERROR][DataCollector::saveSceneInfo]')
            print('\t hfov get failed! please check your camera name and update me!')
            return False

        focal = SIM_SETTING['width'] / 2.0 / np.tan(hfov / 2.0)

        camera_txt = '1 PINHOLE ' + \
            str(SIM_SETTING['width']) + ' ' + \
            str(SIM_SETTING['height']) + ' ' + \
            str(focal) + ' ' + \
            str(focal) + ' ' + \
            str(SIM_SETTING['width'] / 2.0) + ' ' + \
            str(SIM_SETTING['height'] / 2.0)

        with open(self.sparse_folder_path + 'cameras.txt', 'w') as f:
            f.write(camera_txt + '\n')

        points_txt = '1 0 0 0 0 0 0 0 1'
        with open(self.sparse_folder_path + 'points3D.txt', 'w') as f:
            f.write(points_txt + '\n')
        return True

    def createDataset(self, save_dataset_folder_path):
        self.save_dataset_folder_path = save_dataset_folder_path

        if self.save_dataset_folder_path[-1] != '/':
            self.save_dataset_folder_path += '/'

        if os.path.exists(self.save_dataset_folder_path):
            shutil.rmtree(self.save_dataset_folder_path)

        self.image_folder_path = self.save_dataset_folder_path + 'images/'
        self.sparse_folder_path = self.save_dataset_folder_path + 'sparse/0/'
        self.image_pose_file = self.sparse_folder_path + 'images.txt'

        os.makedirs(self.image_folder_path, exist_ok=True)
        os.makedirs(self.sparse_folder_path, exist_ok=True)

        if not self.saveSceneInfo():
            print('[ERROR][DataCollector::createDataset]')
            print('\t saveSceneInfo failed!')
            return False

        return True


    def saveImage(self, image):
        image = (image * 255.0).astype(np.uint8)

        cv2.imwrite(self.image_folder_path + str(self.image_idx) + '.png', image)

        agent_state = self.sim_loader.getAgentState()

        pos = deepcopy(agent_state.position)
        quat = deepcopy(agent_state.rotation)

        matrix = R.from_quat([-quat.x, -quat.y, -quat.z, quat.w]).as_matrix()
        new_pos = - matrix.dot(pos)

        pose_txt = str(self.image_idx)
        pose_txt += ' ' + str(quat.w)
        pose_txt += ' ' + str(quat.x)
        pose_txt += ' ' + str(-quat.z)
        pose_txt += ' ' + str(quat.y)
        pose_txt += ' ' + str(new_pos[0])
        pose_txt += ' ' + str(-new_pos[2])
        pose_txt += ' ' + str(new_pos[1])
        pose_txt += ' 1 '
        pose_txt += str(self.image_idx) + '.png\n'

        with open(self.image_pose_file, 'a') as f:
            f.write(pose_txt + '\n')

        self.image_idx += 1
        return True

    def startKeyBoardControlRender(self, wait_key):
        #  self.resetAgentPose()
        self.cv_renderer.init()

        while True:
            image = self.cv_renderer.renderFrame(self.sim_loader.observations, True)
            if image is None:
                break

            self.saveImage(image)

            self.cv_renderer.waitKey(wait_key)

            agent_state = self.sim_loader.getAgentState()
            print("agent_state: position", agent_state.position, "rotation",
                  agent_state.rotation)

            input_key = getch()
            if not self.keyBoardControl(input_key):
                break
        self.cv_renderer.close()
        return True
