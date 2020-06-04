import os
from flask import Blueprint, jsonify, current_app
from common_tool import get_request_json_obj
from db.docker_model import insert_docker_container, select_docker_by_docker_id, \
    update_container_id_by_docker_id
from shell import run_docker, run_docker_with_sh


docker_blue: Blueprint = Blueprint('docker_api', __name__)


@docker_blue.route('/docker/add', methods=['POST'])
def create_docker():
    """新建容器"""
    create_docker_req = get_request_json_obj()
    # 非空参数校验
    if 'project_id' in create_docker_req:
        project_id = create_docker_req['project_id']
    else:
        return jsonify({'err_no': 202004280848, 'err_msg': 'param error-project_id cannot be null'})
    if 'image_name' in create_docker_req:
        image_name = create_docker_req['image_name']
    else:
        return jsonify({'err_no': 202004280848, 'err_msg': 'param error-image_name cannot be null'})

    docker_dict = {
        'project_id': project_id,
        'image_name': image_name,
        'git_address': create_docker_req.get('git_address', ''),
        'git_branch': create_docker_req.get('git_branch', 'master'),
        'net_name': create_docker_req.get('net_name', ''),
        'net_ip': create_docker_req.get('net_ip', ''),
        'creator_id': create_docker_req.get('creator_id', '')
    }

    err_no, err_msg = insert_docker_container(docker_dict)
    return jsonify({'err_no': err_no})


@docker_blue.route('/docker/run', methods=['POST'])
def run_docker_container():
    """启动docker容器"""
    run_docker_req = get_request_json_obj()
    if 'docker_id' in run_docker_req:
        docker_id = run_docker_req['docker_id']
    else:
        return jsonify({'err_no': 202004301536, 'err_msg': 'param error-docker_id cannot be null'})

    docker_obj = select_docker_by_docker_id(docker_id)
    if docker_obj is None:
        return jsonify({'err_no': 202004301547, 'err_msg': 'cannot find docker record by docker_id'})

    if not docker_obj.image_name:
        return jsonify({'err_no': 202004301550, 'err_msg': 'please configure image firstly'})

    # 执行脚本启动容器
    docker_dict = {
        'image_name': docker_obj.image_name,
        'net_name': docker_obj.net_name,
        'net_ip': docker_obj.net_ip
    }
    container_id = run_docker(docker_dict)

    # 启动脚本后将容器id回写到数据库中
    err_no, err_msg = update_container_id_by_docker_id(docker_id, container_id)
    return jsonify({'err_no': err_no, 'err_msg': err_msg})


@docker_blue('/docker/run/shell', methods=['POST'])
def run_docker_container_with_sh():
    """启动docker容器，并通过挂载shell文件的方式，拉取启动对应项目"""
    run_docker_req = get_request_json_obj()
    if 'docker_id' in run_docker_req:
        docker_id = run_docker_req['docker_id']
    else:
        return jsonify({'err_no': 202005070918, 'err_msg': 'param error-docker_id cannot be null'})

    docker_obj = select_docker_by_docker_id(docker_id)
    if docker_obj is None:
        return jsonify({'err_no': 202005070919, 'err_msg': 'cannot find docker record by docker_id'})

    if not docker_obj.git_address:
        return jsonify({'err_no': 202005070920, 'err_msg': 'please configure git_address firstly'})

    if not docker_obj.image_name:
        return jsonify({'err_no': 202004301521, 'err_msg': 'please configure image firstly'})

    docker_dict = {
        'image_name': docker_obj.image_name,
        'net_name': docker_obj.net_name,
        'net_ip': docker_obj.net_ip
    }
    container_id = run_docker_with_sh(docker_dict)

    # 启动脚本后将容器id回写到数据库中
    err_no, err_msg = update_container_id_by_docker_id(docker_id, container_id)
    return jsonify({'err_no': err_no, 'err_msg': err_msg})
