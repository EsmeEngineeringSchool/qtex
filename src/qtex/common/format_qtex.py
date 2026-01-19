"""
    les différentes entrées qui peuvent être lues dans un fichier au format qtex.
    La clé du dictionnaire correspond au différent entrée reconnue au format #clé
    Cette clé possède trois propriétés :
        long        : oui ou non l'entrée est multilignes c'est à dire qu'elle commence par #key et #END key 
        translation : oui ou non l'entrée est traduisible (ça a du sens de la traduire)
        multiple    : oui ou non l'entrée est répétée dans le fichier
"""
entrees={'TYPE'                    :{'long':False,'translation':False,'multiple':False},
         'NAME'                    :{'long':False,'translation':True ,'multiple':False},
         'Q'                       :{'long':False,'translation':True ,'multiple':False},
         'Q_LONG'                  :{'long':True ,'translation':True ,'multiple':False},
         'EXTRA_Q_LONG'       :{'long':True ,'translation':True ,'multiple':False},
         'Q_IMG'                   :{'long':False,'translation':False,'multiple':False},
         'GFBACK_LONG'             :{'long':True ,'translation':True ,'multiple':False},
         'GFBACK'                  :{'long':False,'translation':True ,'multiple':False},
         'CFBACK'                  :{'long':False,'translation':True ,'multiple':False},
         'PFBACK'                  :{'long':False,'translation':True ,'multiple':False},
         'IFBACK'                  :{'long':False,'translation':True ,'multiple':False},
         'SUB_Q'                   :{'long':False,'translation':True ,'multiple':True },
         'SUB_Q_LONG'              :{'long':True ,'translation':True ,'multiple':True },
         'ANSW_GRAD'               :{'long':False,'translation':False,'multiple':True },
         'ANSW_TEXT'               :{'long':False,'translation':True ,'multiple':True },
         'ANSW_TEXT_LONG'          :{'long':True ,'translation':True ,'multiple':True },
         'ANSW_FBACK'              :{'long':False,'translation':True ,'multiple':True },
         'ANSW_IMG'                :{'long':False,'translation':False,'multiple':True },
         'TAGS'                    :{'long':False,'translation':False,'multiple':False},
         'CR_TYPE'                 :{'long':False,'translation':False,'multiple':False},
         'CR_ISCOMBINATORTEMPLATE' :{'long':False,'translation':False,'multiple':False},
         'CR_PENALTYREGIME'        :{'long':False,'translation':False,'multiple':False},
         'CR_ACELANG'              :{'long':False,'translation':False,'multiple':False},
         'CR_TWIGALL'              :{'long':False,'translation':False,'multiple':False},
         'CR_PRELOAD'              :{'long':True ,'translation':False,'multiple':False},
         'CR_TEMPLATE'             :{'long':True ,'translation':False,'multiple':False},
         'CR_ANSWER'               :{'long':True ,'translation':False,'multiple':False},
         'CR_CASE_MARK'            :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_CODE'            :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_CODE_LONG'       :{'long':True ,'translation':False,'multiple':True },
         'CR_CASE_STDIN'           :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_DISPLAY'         :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_EXTRA'           :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_ASEXAMPLE'       :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_EXPECTED'        :{'long':False,'translation':False,'multiple':True },
         'CR_CASE_EXPECTED_LONG'   :{'long':True ,'translation':False,'multiple':True },
         'STACK_QVAR'              :{'long':False,'translation':False,'multiple':False},
         'STACK_SFBACK'            :{'long':False,'translation':False,'multiple':False}
} 

# entrees par type 
globalinfo           = ['TYPE','NAME']
questioninfo         = [('Q','Q_LONG'),('GFBACK','GFBACK_LONG'),'TAGS','Q_IMG','EXTRA_Q_LONG']
multichoiceinfo      = ['CFBACK','PFBACK','IFBACK','ANSW_FBACK','ANSW_GRAD',('ANSW_TEXT','ANSW_TEXT_LONG'),'ANSW_IMG']
numericalinfo        = ['ANSW_FBACK','ANSW_GRAD','ANSW_TEXT']
coderunnerinfo       = ['CR_TYPE',\
                        'CR_ACELANG',\
                        'CR_TWIGALL',\
                        'CR_PENALTYREGIME',\
                        'CR_ISCOMBINATORTEMPLATE',\
                        'CR_TEMPLATE',\
                        'CR_PRELOAD',\
                        'CR_ANSWER',\
                        'CR_CASE_MARK',\
                        ('CR_CASE_CODE','CR_CASE_CODE_LONG'),\
                        ('CR_CASE_EXPECTED','CR_CASE_EXPECTED_LONG'),\
                        'CR_CASE_DISPLAY',\
                        'CR_CASE_STDIN',\
                        ('CR_CASE_EXTRA','CR_CASE_EXTRA_LONG'),\
                        'CR_CASE_ASEXAMPLE']
stackinfo            = ['STACK_QVAR','STACK_SFBACK']
shortanswerwirisinfo = ['ANSW_FBACK','ANSW_GRAD','ANSW_TEXT']
multichoicewirisinfo = []
matchinginfo         = ['CFBACK','PFBACK','IFBACK',('ANSW_TEXT','ANSW_TEXT_LONG'), ('SUB_Q','SUB_Q_LONG')]


infos={"global"           : globalinfo ,  \
       "description"      : questioninfo, \
       "question"         : questioninfo, \
       "multichoice"      : multichoiceinfo,\
       "numerical"        : numericalinfo,\
       "coderunner"       : coderunnerinfo,\
       "stack"            : stackinfo, \
       "multichoicewiris" : multichoicewirisinfo,\
       "shortanswerwiris" : shortanswerwirisinfo,\
       "matching"         : matchinginfo,
       "shortanswer"      : multichoiceinfo
      }

# entrées multiples exigées de même taille et au moins une doit être présente
types_with_requirements = ["multichoice","numerical","coderunner","matching"]
same_number={"multichoice" :[ 'ANSW_FBACK','ANSW_GRAD','ANSW_TEXT',"ANSW_IMG"],
             "numerical"   :[ 'ANSW_FBACK','ANSW_GRAD','ANSW_TEXT'],
             "matching"    :[ 'ANSW_FBACK','ANSW_GRAD','ANSW_TEXT', "SUB_Q"],
             "coderunner"  :[ 'CR_CASE_MARK','CR_CASE_CODE','CR_CASE_ASEXAMPLE','CR_CASE_EXPECTED',
                              'CR_CASE_DISPLAY','CR_CASE_STDIN','CR_CASE_EXTRA']}
