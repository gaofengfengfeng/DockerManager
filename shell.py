from common_tool import gen_unique_id
import os

ROOT_DIR = 'static/shell/'


def test_git_pull():
    """调用脚本 从git拉取java项目，并创建镜像启动"""
    sh_file_path = ROOT_DIR + 'centos_jdk_test.sh'
    git_address = 'https://github.com/gfffbjtu/SpringBootTest.git'
    git_branch = 'master'
    image_name = 'dockerjava:v3'
    param_arr = ['sh', sh_file_path, git_address, git_branch, image_name]
    os.system(' '.join(param_arr))


def build_java_project_image(image_dict):
    """调用脚本 从git拉取java项目,返回生成的镜像id"""
    sh_file_path = ROOT_DIR + 'build_java_image.sh'
    git_address = image_dict['git_address']
    git_branch = image_dict['git_branch']
    image_name = image_dict['image_name']
    tmp_file = gen_unique_id()
    param_arr = ['sh', sh_file_path, git_address, git_branch, image_name, '>', tmp_file]
    os.system(' '.join(param_arr))
    file = open(tmp_file)
    lines = file.readlines()
    tail_line = lines[-1]
    os.system('rm -rf ' + tmp_file)
    image_id = tail_line.split(' ')[-1]
    if image_id.endswith('\n'):
        return image_id[0: -1]
    return image_id


def run_docker(docker_dict):
    """调用脚本，根据指定镜像启动docker容器"""
    sh_file_path = ROOT_DIR + 'run_docker.sh'
    tmp_file = gen_unique_id()
    param_arr = [
        'sh',
        sh_file_path,
        docker_dict.get('image_name'),
        docker_dict.get('net_name', ''),
        docker_dict.get('net_ip', ''),
        '>',
        tmp_file
    ]
    os.system(' '.join(param_arr))
    file = open(tmp_file)
    lines = file.readlines()
    container_id = lines[-1]
    os.system('rm -rf ' + tmp_file)
    if container_id.endswith('\n'):
        return container_id[0: -1]
    return container_id


def run_docker_with_sh(docker_dict):
    """启动docker容器，并通过挂载shell文件的方式，拉取启动对应项目"""
    shell_file_name = ROOT_DIR + 'run_docker_with_volumn.sh'
    tmp_file = gen_unique_id()
    param_arr = [
        'sh',
        shell_file_name,
        docker_dict.get('image_name'),
        docker_dict.get('net_name', ''),
        docker_dict.get('net_ip', ''),
        '>',
        tmp_file
    ]
    os.system(' '.join(param_arr))
    file = open(tmp_file)
    lines = file.readlines()
    container_id = lines[-1]
    os.system('rm -rf ' + tmp_file)
    if container_id.endswith('\n'):
        return container_id[0: -1]
    return container_id


if __name__ == '__main__':
    docker_dict = {
        'image_name': 'dockerjava:v6',
        'net_name': '',
        'net_name': ''
    }
    run_docker(docker_dict)
