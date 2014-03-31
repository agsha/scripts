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
    vlg_cookie = "3guep4gpuegla516328kvsj3qmwwgsw2"
    vlg_tc_lirary_org = ["http://vlg-cloud.tc-library.org/",
            "http://vlg-cloud.tc-library.org/vialogues/play/6947/",
            "http://vlg-cloud.tc-library.org/vialogues/play_embedded/6947/",
            "http://vlg-cloud.tc-library.org/vialogues/play/7293/",
            "http://vlg-cloud.tc-library.org/vialogues/play_embedded/7293/",
            #"http://vlg-cloud.tc-library.org/videos/embedded/11257/",
            "http://vlg-cloud.tc-library.org/profiles/user/Katezvdp/",
            "http://vlg-cloud.tc-library.org/search/advanced/?sort=&exclude=&participants=voice&sort=created/",
            "http://vlg-cloud.tc-library.org/search/advanced/?tags=developer&title=&participants=&description=&exclude=/",
            #"http://vlg-cloud.tc-library.org/vialogues/create?id=11422#/embed_vimeo/",
            "http://vlg-cloud.tc-library.org/vialogues/create/",
            "http://vlg-cloud.tc-library.org/vialogues/explore/",
            "http://vlg-cloud.tc-library.org/videos/browse/",
            "http://vlg-cloud.tc-library.org/notification/",
            "http://vlg-cloud.tc-library.org/groups/user/pranav_garg/",
            "http://vlg-cloud.tc-library.org/groups/create/",
            "http://vlg-cloud.tc-library.org/vialogues/pranav_garg/favorites/show/",
            "http://vlg-cloud.tc-library.org/notification/settings/",
            "http://vlg-cloud.tc-library.org/support/",
            "http://vlg-cloud.tc-library.org/release_notes/",
            "http://vlg-cloud.tc-library.org/support/help/what_is_vialogue/",
            "http://vlg-cloud.tc-library.org/support/contactus/",
            "http://vlg-cloud.tc-library.org/profiles/admin/",
            "http://vlg-cloud.tc-library.org/vialogues/browse/related/6448/",
            "http://vlg-cloud.tc-library.org/vialogues/manage/7282/",
            
            #APISs
            "http://vlg-cloud.tc-library.org/vialogues/api/discussions/",
            "http://vlg-cloud.tc-library.org/vialogues/api/discussions/6947",
            "http://vlg-cloud.tc-library.org/vialogues/api/rec_discussions/"
            "http://vlg-cloud.tc-library.org/vialogues/api/comments/?discussion=6947"
            "http://vlg-cloud.tc-library.org/vialogues/api/polls/?discussion=6947"
            
            "http://vlg-cloud.tc-library.org/videos/api/videos/",
            "http://vlg-cloud.tc-library.org/videos/api/videos/6498",
            "http://vlg-cloud.tc-library.org/vialogues/api/profile_discussions/1",
            "http://vlg-cloud.tc-library.org/vialogues/api/my_discussions/",
            "http://vlg-cloud.tc-library.org/favorites/api/",
            "http://vlg-cloud.tc-library.org/notification/api/notices/0/unseen",
            "http://vlg-cloud.tc-library.org/notification/api/notices/"
            
            ]
    
    
    prod_vialogue_cookie="f2123808c7992b4655f3b4ea382e523e"
    vialogues_com_urls = ["https://vialogues.com/",
            "https://vialogues.com/vialogues/play/6947/",
            "https://vialogues.com/vialogues/play_embedded/6947/",
            "https://vialogues.com/vialogues/play/11005/",
            "https://vialogues.com/vialogues/play_embedded/11005/",
            #"https://vialogues.com/videos/embedded/11257/",
            "https://vialogues.com/profiles/user/Katezvdp/",
            "https://vialogues.com/search/advanced/?sort=&exclude=&participants=voice&sort=created/",
            "https://vialogues.com/search/advanced/?tags=developer&title=&participants=&description=&exclude=/",
            #"https://vialogues.com/vialogues/create?id=11422#/embed_vimeo/",
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
            "https://vialogues.com/vialogues/browse/related/11818/",
            "https://vialogues.com/vialogues/manage/11818/"
            ]
    
    urls = vlg_tc_lirary_org
    cookie = vlg_cookie
    result_file = open("ab_results.csv", "w")
    result_file.write("url#ab_command#document_length#min#mean#std_dev#median#max\n")
    concurrency = 2
    requests = 10
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
                
        
    
    
    
    