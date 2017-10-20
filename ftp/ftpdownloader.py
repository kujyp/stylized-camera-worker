import os
from ftplib import FTP, error_perm

from auth import ftp_account


def downloadtraineddatafromftp(traindir):
    ftp_domain = ftp_account.DOMAIN
    ftp_user = ftp_account.ACCOUNT
    ftp_pwd = ftp_account.PASSWORD
    ftp_homepath = ftp_account.HOMEPATH
    ftp_targetpath = "trained_data"
    ftp_downloadlocaldir = convert_path_sep(traindir)

    # mkdir in local
    local_dir = ftp_downloadlocaldir
    mkdir_unless_exist(ftp_downloadlocaldir)

    # ftp connect
    ftp = FTP(ftp_domain)
    print('Connecting FTP Server : \t\t' + ftp_domain)
    ftp.encoding = "utf-8"
    ftp.login(ftp_user,ftp_pwd)

    ftp_path = (ftp_homepath + '/' + ftp_targetpath)
    print('Connecting FTP Dir : \t\t' + ftp_path)
    everydirnames = get_everydirnames(ftp, ftp_path)
    ftp_relpaths = get_everyrelpath_fromftp(ftp, ftp_path)

    # Download all files
    for ftp_relpath in ftp_relpaths:
        filename = ftp_relpath.split('/')[-1]
        dirnames = ftp_relpath.split('/')[1:-1]

        ftp_curpath = ftp_path
        local_path = local_dir
        for dirname in dirnames:
            ftp_curpath = ftp_curpath + '/' + dirname
            local_path = os.path.join(local_path, dirname)

        local_pathwithfilename = os.path.join(local_path, filename)
        if os.path.isfile(local_pathwithfilename):
            print('Exist file : \t\t\t\t' + local_pathwithfilename)
        else:
            try:
                mkdir_unless_exist(local_path)
                ftp.cwd(ftp_curpath)
                print("Downloading ... \t\t\t" + local_pathwithfilename, end='')
                ftp.retrbinary('RETR %s' % filename, open(local_pathwithfilename, 'wb').write)
                print(" - Completed")
            except:
                print("retry .", end='')
                import time
                time.sleep(1)
                print(".", end='')
                time.sleep(1)
                print(".")
                time.sleep(1)
                ftp.retrbinary('RETR %s' % filename, open(local_pathwithfilename, 'wb').write)

    ftp.quit()
    return everydirnames


def convert_path_sep(local_path):
    return local_path.replace("/", os.sep)


def mkdir_unless_exist(local_path):
    dirs = local_path.split(os.sep)
    path = ''
    for dir in dirs:
        if dir == '':
            # it means ABSOLUTE PATH
            path = '/'
            continue

        next_path = path + dir + os.sep
        try:
            os.stat(next_path)
        except:
            print('Make dir : \t\t\t\t\t' + next_path)
            os.mkdir(next_path)
        path = next_path


def get_everydirnames(ftp, path):
    ftp.cwd(path)

    ftp_paths = ftp.nlst()

    everydirnames = []
    for ftp_path in ftp_paths:
        # ftp.cwd(path)
        try:
            ftp.cwd(ftp_path + "/")
            dirname = os.path.basename(ftp_path)
            everydirnames.append(dirname)
            print("Dirname : %s" % dirname)
        except error_perm:
            print("not dir")
            pass

    return everydirnames


def get_everyrelpath_fromftp(ftp, path):
    ftp_fullpaths = get_everypath_fromftp(ftp, path)
    ftp_relpaths = []
    ftp_abspathlen = len(path)
    for ftp_fullpath in ftp_fullpaths:
        ftp_relpath = ftp_fullpath[ftp_abspathlen:]
        ftp_relpaths.append(ftp_relpath)
    return ftp_relpaths


def get_everypath_fromftp(ftp, path):
    ftp.cwd(path)

    ftp_paths = ftp.nlst()

    everypath = []
    for ftp_path in ftp_paths:
        dir_flag = False
        try:
            ftp.cwd(ftp_path + "/")
            dir_flag = True
            everypath += get_everypath_fromftp(ftp, ftp_path + "/")
        except error_perm:
            if not dir_flag:
                everypath.append(ftp_path)
                #print ftp_path
    return everypath
