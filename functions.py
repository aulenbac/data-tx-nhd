class Nhd:

    def build_nhd_repo_directory_listing(sbitemid, ftpurl):
        from ftplib import FTP
        from datetime import datetime
        from time import strptime

        ftpSite = ftpurl.replace('ftp://', '').split('/')[0]
        ftpDir = '/'.join(ftpurl.replace('ftp://', '').split('/')[1:])

        ftp = FTP(ftpSite)
        ftp.login()
        ftp.cwd(ftpDir)

        ftpDirList = []

        ftp.dir(ftpDirList.append)

        ftp.quit()

        nhdRepositoryListing = {}
        nhdRepositoryListing['Source ScienceBase Item'] = sbitemid
        nhdRepositoryListing['FTP Server'] = ftpSite
        nhdRepositoryListing['FTP Directory'] = ftpDir
        nhdRepositoryListing['Date Retrieved'] = datetime.now().isoformat()

        nhdRepositoryListing['File Catalog'] = []
        for line in ftpDirList[2:]:
            dirList = list(filter(None, line.split(' ')))

            thisItem = {}
            thisItem['File Name'] = dirList[-1]
            thisItem['File Size'] = dirList[4]
            thisItem['File Date'] = datetime(year=int(dirList[7]), month=strptime(dirList[5], '%b').tm_mon,
                                             day=int(dirList[6])).isoformat()

            if thisItem['File Name'][0:7] == 'NHDPlus':

                filePartToWork = thisItem['File Name'].split('.')[0]
                fileStartStuff = filePartToWork.split('_')[0].replace('NHDPlus', '').split('V')
                thisItem['NHD Version'] = fileStartStuff[1]

                possibleNHDRegion = fileStartStuff[0]
                try:
                    if possibleNHDRegion[0].isdigit() and possibleNHDRegion[1].isdigit():
                        thisItem['NHD Processing Unit'] = possibleNHDRegion
                except:
                    pass

                possibleFileVersion = filePartToWork.split('_')[1]
                if possibleFileVersion[0].isdigit() and possibleFileVersion[1].isdigit():
                    thisItem['File Version'] = possibleFileVersion

                thisItem['File Type'] = '_'.join(filePartToWork.split('_')[2:])

            nhdRepositoryListing['File Catalog'].append(thisItem)

        return nhdRepositoryListing