'''
Created on Jun 24, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
import sys
from os.path import expanduser, exists

if __name__ == '__main__':
    cookie = "kf689v8lt3ja7l7t3a4q6fx97gfoqdfz"
    urls = ["https://vialogues.com/",
            "https://vialogues.com/vialogues/play/11211/",
            "https://vialogues.com/vialogues/play_embedded/11211/",
            "https://vialogues.com/vialogues/play/12080/",
            "https://vialogues.com/vialogues/play_embedded/12080/",
            "https://vialogues.com/videos/embedded/11257/",
            "https://vialogues.com/profiles/user/Katezvdp/",
            "https://vialogues.com/search/advanced/?sort=&exclude=&participants=voice&sort=created/",
            "https://vialogues.com/search/advanced/?tags=developer&title=&participants=&description=&exclude=/",
            "https://vialogues.com/vialogues/create?id=11422#/embed_vimeo/",
            "https://vialogues.com/vialogues/create/",
            "https://vialogues.com/vialogues/explore/",
            "https://vialogues.com/videos/browse/",
            "https://vialogues.com/notification/",
            "https://vialogues.com/groups/user/pranav_garg/",
            "https://vialogues.com/groups/create/",
            "https://vialogues.com/vialogues/pranav_garg/favorites/show/",
            "https://vialogues.com/notification/settings/",
            "https://vialogues.com/support/",
            "https://vialogues.com/release_notes/",
            "https://vialogues.com/support/help/what_is_vialogue/",
            "https://vialogues.com/support/contactus/",
            "https://vialogues.com/profiles/admin/",
            "https://vialogues.com/vialogues/browse/related/11408/",
            "https://vialogues.com/vialogues/manage/12868/"
            ]
    result_file = open("ab_results.csv", "w")
    result_file.write("url#ab_command#document_length#min#mean#std_dev#median#max\n")
    concurrency = 2
    requests = 2
    for url in urls:
        cookie_cmd = ""
        if len(cookie)>0:
            cookie_cmd = """ -H "Cookie: sessionid=%s" """%(cookie)
        cmd = "ab -n %s -c %s %s %s"%(requests, concurrency, cookie_cmd, url)
        out, err, ret = exec_command(cmd)        
        for line in out:
            if line.startswith("Total:"):
                l = line.split()
                times = ( "%s#%s#%s#%s#%s"%(l[1], l[2], l[3], l[4], l[5]) )
            if line.startswith("Document Length:"):
                l = line.split()
                doc_length = ( "%s"%(l[2]) )
        
        result_file.write("%s#%s#%s#%s\n"%(url, cmd, doc_length, times))
                
        
    
    
    
    