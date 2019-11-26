#! /bin/bash
#
# recive_repo.sh
# Copyright (C) 2019 luominghao <luominghao@live.com>
#
# Distributed under terms of the MIT license.
#

# 基于rsync，同步指定的目录

RSYNC_SERVER_IP=
RSYNC_USERNAME=
RSYNC_PASSWORD=
RSYNC_SRC_DIR=
RSYNC_SRC_PATH=
RSYNC_DES_PATH=
RSYNC_WORK_DIR=

get_rsync_modules()
{
    return 0
}

get_module_children()
{
    return 0
}

get_rsync_dir_list()
{
    # 获取每个module的子目录，生成module/dir形式的列表
    local modules=
    local module=
    modules=$(get_rsync_modules)
    if [[ $? -ne 0 ]]; then
        echo "get rsync server(${RSYNC_SERVER_IP}) modules failed"
        return 1
    fi

    local module_children=
    for module in $modules
    do
        module_children=$(get_module_children "${module}")
        if [[ $? -ne 0 ]]; then
            echo "get module(${module}) children failed"
            return 1
        fi

        echo "${module_children}"
    done
    
    return 0
}

get_user_selects()
{
    return 0
}

get_one_sync_dir()
{
    if [[ -n $RSYNC_SRC_DIR ]]; then
        echo "${RSYNC_SRC_DIR}"
        return 0
    fi

    local dir_list=
    dir_list=$(get_rsync_dir_list)


    local dir_name=
    dir_name=$(get_user_selects "${dir_list}")
    if [[ $? -ne 0 ]]; then
        echo "get rsync src dir failed"
        return 1
    fi

    echo "${dir_name}"
    return 0
}

get_rsync_src_path()
{
    local dir_name=
    dir_name=$(get_one_sync_dir)
    if [[ $? -ne 0 ]]; then
        echo "get rsync src dir failed"
        return 1
    fi

    echo "rsync://${RSYNC_USERNAME}@${RSYNC_SERVER_IP}/${dir_name}"
    return 0
}

rsync_dir()
{
    return 0
}

get_sync_des_path()
{
    echo "${RSYNC_WORK_DIR}"
    return 0
}

main()
{
    return 0
}

main "$@"
