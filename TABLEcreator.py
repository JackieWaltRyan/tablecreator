from base64 import b64encode
from json import loads, dump, dumps
from os import walk, makedirs
from os.path import exists
from sys import exit

from bs4 import BeautifulSoup

FAKE_ALL = str("iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAJ5ElEQVR42u2bC3BU1RnHs5sXJEACJkAKhHcpFSsMCFWpDoyv8dHp"
               "Y9RSxbZ2ZGrFFoulVVrpgK2RR+toLYNVwJFR22m1VkUGgQCVgtDhIdUKyCOP3U3CPpLdJJv36e/Od2bO3dxd2WgICcmZ+c3d3XvO"
               "uef7n+8759y796QopXo1KSqlvCtIgyzIgWEwCsbAOBgLhVAAl8BAyAR3F7TrvAng0gYPhykwB+6EhfBreBKegmfgaVgNK+Bh+D7c"
               "AjO0SDmQ3lMESIehMA1uh1/BengH9sEx8EAAwhDRhKASTsNh2AF/0cLcB9fCaMgGV3cUIB1GwBzdiy9pg8uhHlqgDVSStEIzBOFD"
               "eAtWwndgMgzoLgK4IV8b/hhs1r0YNQZ3Ci3g16Kuhe/CRMi8kAJkweWwCN4Ej26oOo+0QRj2wxq4CfK6WgCX7vWbdW+cgCZQXUgb"
               "BGAL3A9fhPSuEMANhfBD7e5BUBeQFjgKRTAT+p1PAVJhAiyG/abXuwXl8DzMhazOF8AYvxQ+hlZQ3YwQvArXdUSEZGN+PDwCx0F1"
               "Y8LwivaEfp0lQAE8CB+B6gHUwAaYCWmfV4BcmAd7zLzeI/DBKj07uD6rABnwNXjNDHg9io9hIQzuuAAm7osgBKoH0gLFcCNkdFSA"
               "QXA3/BdUDyYMa2FCRwRIhamwSauoejj/g3sgO1kBcmEBlIC6CIjCyzA5GQHccBm8ZBY7FwXHdEj3P5cA2TBPu426iKiBdTD6XAIU"
               "wpPQCMpQZuB7MueceUqFz2FIh69n8rTC+zAXUhMJkApXwmZHZamlwNFlVVoSi4vfB5NvQCKDS6T8BK9ShZDRPl+JE8ppnMamQbqu"
               "35nf/D7Co1QeuKUceGARDEokwAAdJydBCmXCTZVKPRJU6ucBpRb4lfqKT6npFUpdDrM5t5jfXwwr9UBALp7BRYfDCCiE6eR/lPK7"
               "G5T6R51S03zGqOEIciX1zIDpmlnUOYXjeM5N8kk9qTZjv31WqeUhpX5KW66tpL4KK5/kH6NF/laVUm9zrSfIN5DyYk8ENsKYRAIU"
               "wDKIghTqD0VUUtuqVLBFKS/sbVTqQJNS78MHUM1vqk2pN+opc0apAo+U2cb37Ri9n/w1rUoSx/l+02s30ND/NEh9+zUHYR2CvhBB"
               "NMr+rZYOCGDUWRH0z5xr5Jp+OKLbYeUrjir1bj3X5XiySS73CXV/wStiy5S+R3u5ywggX9wwGdaD0ojbX1cpRjqTGN4EVnqnQQQY"
               "Ui497m2On/8nQS0AdY8pp1ydM9u6aqX2Rc33aKsYvCQkHnkcA5NJPvKN0h5nlsd3QIZdgDTN1bAFVAxuCj8eiq34MMb+jkauhpcj"
               "4gmv1VmGSczlUeZH9FpDq3Kkn4kA1C3HWzAoYBP477UYSm+X2QQ8yecVtOEan5R5tia2zn81UI7rF3Mss9VV34bIFXYBymAxDLQL"
               "kKm5DQ7FHVEv48LNbabiTRHp7ftw55WIMKtC4k4uJOdmUKYmjhc8RuM5b+rGrT9sMOdXc35j2HwvaSLuq2IHySUB2mMT93bOFxJS"
               "46nzbsR7FREbdXsnxgjghzWQbxcgC7JhPpyJK8BI4uiUze12R+k5Kj7SSNxacUYet32K4/P1NKopjgc8FYkVIJfj1npz/kSTNdYY"
               "11+IsRIypsx8jAzZenqW5RmnlPoqYt5mDaAc14app4nPMQJE4EUYbRdgEOTA/eCPK8AwBNhpi9U61C3RvevlONdnn+Olwd/wm/zV"
               "EsMkCZUs+9RG3qcjKm5ahXely4AZ056rMOq0rUP+UMPY4pfQ/ADyPHSa9oYcj92eBngDJtkFGAxD4CEIxxVgKAJsEwEcqRQB5tgH"
               "Gu0NvwzpXkSst3HJXbqXD+A94zyx4bI8JqZN7z8YYBATj4qpfwrtOWYTIEze2hYz8I3zJVp4NcNWmAIuixRt/CWwBGoTesAumwCn"
               "m/VApD1hstfeQJm7i3X+M030pLUO0AIcJ2xm2j0GAX4rMU91MvhFMKa1TYx8i3J3VMmCK0UzyytTXbx0MCohK6LFE2A7TO2YAMYD"
               "zKibh2u+guu+x2e3/WJ8vrpSjCARz4hRb0IgiIG3VsUVAKNlzv+BX4SVJMbO5/dM3Z5bqd9nO/9P2vYMHXIUcffyeZiHMKP+XI7u"
               "cwiQRAiIBxS3EyDltFJf8hJnfmOMCCBzfaLUhpE/Dpip0MXxuYhZJ9xYKQPa8pBeY+h0yAod6VlWpOLykkTQAXrN8nXIp96lQabc"
               "AL8nCgEzBuRA7qcOgiO89IjN5f7daEZmN9iNn4jqh6PGoI/Iu6GWo618kW0qLADCQyfECYoAV/lir3mUOid5pRxrEMtbSLJIm+Cx"
               "ymho1y9CMi68V4cYJjwTDYLZMODTpkHmeTFGkhgzTOIRTL4ceLY6duX3eBCRTiq1zDbQbaFhefqGZjaGljeac3/FG/qXijCHbOuD"
               "P4Z1byLA6zZvPEXZGyrwDs5dihAPB80UuadewjfONJjkQqhM4u55Lm6S3Bv8JqRjX+dLB2thVN9u2bwxwvlPlLonYJsWmyWOUxDm"
               "e2dj1ws1LRIGBdR3xCbAPL+E3cwYz5D7jJ1RuRfZRv56W12bwnSKsQf8sBry4y2FZzuWwi4dV/SkI51o0KO/FmAgx/XSy+Q3RGjQ"
               "9dSxoN24sKyaHqPcrqiz7s308DVeWXBJonxABFsVUkmnDVxjkNjiXAo7b4a+7LgZygCrVw/qO7V9uNu7NOpNGvgnjJ1pm/8z4ZtV"
               "1jJWWG8dI3JcEZA7NXs62mTVJVPqDsTczudi2Mnn12uZ6z2EQ63Jv5dz99KWrXW0R7djBxRbNEgd3KnSTuEArLEEkIWQ42Yoqdvh"
               "NJjglTFgBkyDsR7zsCErzo3TYI5DIR/yYAi/rdMhVIc3VOlbWeve4iQNvuusNbqDR641ESbp0X5RUFzaJAmxJUHJP95LGc04mGq1"
               "U3OFfk6QJm1z3g4nfiByyjEOJH5ac47HX+QfVm7dw0vPPkGPPEAvPhQgBEKMCxifXeqsV+oWkVdWy7S7W2AAlHEj01zHUGKnffvC"
               "53ogkmZ/JNY5lIkLXurDc7wYqxudqpfLGWWmh5yYsWWi7uWxMNIjT336eTranrLEj8QMhVAEjaA6CWfPGpIT0ekdHbi286Fo32Px"
               "JP8Yaetdf4w4/xorvdj+Guv7c7Tv7/G+FyT6XpHpLS9JVdhfkuqNr8lthCsgre9FyU5+VfbRbvyqbPD8vCprcPXel6UNbhgF93aT"
               "1+Wbu/B1eUM32TDhd2yYuMBbZrxduGXmAPzebJm58Jum5nbxpqm7dK9nXuzb5kLtts3dabbN9YyNk0vhBdicYONkbc/cOJn81tmC"
               "3rV1NvnN0yNhbHfYPN3rt8//H0EYXlIdCHPBAAAAAElFTkSuQmCC")

FAKE_PONY = str("iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAABED0lEQVR4XuzUwREAEBAEsGV8VK8EpZ4mvEiKSKuq/AnouQcQACAA"
                "QACAAAABAAIABAAIABAAIABAAIAAAAEAAgAEAAgAEAAgAEAAgAAAAQACAAQACAAQADDykD1XXnHY+/NoTa6zsPf/Pnvvqnqn8565"
                "50E9Sq3Rsi1ZYHkEgw22McSYIRB+hoDhAhmBJAQMIeESphCm5HKdRbDh4hsCBnNjsAHJtjzKo2xZY3er5/HMwztU1d77+YmcXuqW"
                "JbXUrT59zrHro/Wso/VqnT5Hf9R3Ve3aVR2J1LXGWBxmUNsIQp+cGZnjmDuFxXBbeTOfTe7ner+XRbqcMRNsD5v4YvIwG8N6XuRv"
                "4oyZ5H73MC/0N3JzuI6/Se/hmDnFdeUuBmjy8fRzGDWkmuCw1MhoxDpNrdPQBuNxhDN2Sj6YfNwumEXxeLbFzfZDySfjMXOy+OPZ"
                "3+KEOU1WqyEt93rvwj+J3i9M1ubfcevUdffkJu8ea55hMenhTWD7wgZOtCZY3x1hoGxwZOAk1yxs5kj7DN3uaZrj19G+5nbSqXms"
                "h7QQnBesBxN5KoHgoHRKnilFBtGCd1AmkVvvS+lnyqEdnrQQ9jzqOLo9cGYjmKBsOSY0O8JD+zwuWpwXBEEFglFe87fXVAH4ylMR"
                "BEXpSBfB7M1INjrcSCRuFpHNFjPq1A0tSrfR1mb6uuKVblSHHVh6dOK+cnfsSx460uv36E8ULuR7ujtuHi/WvwAtQmnidSXF9Ex9"
                "7lDfFh/r2fxub8J+RVkBlSoAFUHoS2470n354/PiwTiw/jX5y4ZT0s1WTVuQpsMOO9xgoq7lcCZRR0ZKQxs4BgADLLAv7MYgTMgM"
                "63QUeuLX+VFXi20gAnJ9bhZx6u5cX4zeWRj/ptwWR+bs4tFF1/3DEdM+JgjLpFIFoCIIgUAu+Q2ecFNBme3xO3aMmpGvH48jd6yL"
                "o3a9bgYc5+lFpssSi8UBsE43AAYKdeCBPiAAZLHGurwJudkBsgNKjjaOYyXZ1SiTj3Vc92Bp/Ie5cipVACqB6CJxs8e3m9rYtilu"
                "fGtbW/8gorzA3wo4wAMRKIGCSxM5L/BkwnkRiJwnbOtufXx2f3/fTH3/Q4OHHxzNB/+NogeDxIOK9rkslSoAFQEsUEtJbk5wP5NL"
                "8Zpr4w73wvxWwAMKFEuzIhTwgKcWa9w6c8P1Xor3PtQ+OGHVfL/BfADwgPLcVKoAVATB40cXzeKPZD771n/Yf9OGjNqIU+sSHBBY"
                "nSJOLdct7Bjf1dn7+591H/yDExt6v9GGUzy7ShWASke6m6dl7kev97tfdku4ec+g1tcP6jBLIqBAZHVSAJKYkcR0fEN953fPNuVI"
                "N/N3keorrWFIlGGFZoTURhygX9a+6B1FmWinSPVsnnI2Oqa9Y6JI9TEVzgpfIaoAVAShxNOTIguEf/Wy4iU3Dcfhb7ombm442kAO"
                "eNaWCPTZVGzcXD8qP1pOhtclveRGibRsoGWiZCaCKE8lEA1Eo4W3zEbLvBoWomEuGD2TFnJkoanTRaqfE+UeIGctqgJQEYSe9AdH"
                "dPDW8TD+tet07N/tCLsBB/SBRUBYq5p5jeYp9kHcB45LlALrlua8IlXyVNl0yn3aBv48Gr4ULNPe8UmnhCoAa0YlENYZMd91q7/p"
                "p2/2L1kHi1+2qCesbZHzlCshLWDjWfv4uNtAb5sYDjS6crA9z094q5+LhkmgWz0LsOpV+vT/00vKF/ynm/yN4zALeJ6rigIwPmO5"
                "4eFk50s/6v5s40nz12XCt7CaVQGoKEpO8VcvjDe9aXPcYoQgXLaKKJIEMXsec9ftfsz9ei/jf+apDqhUlwCrTnV7L2yIxN+9Lux6"
                "3biOAQYIPH+VtBDz+GyUyLcNdkzroX3xN4uU99dyUKnOAFZQRRByybcmuH+zPW7/tnFdD8gyHPyV9qI1m0+61+7db3+u0ZW39DPN"
                "RKszgBVUKSlHRnTordfEa/7J5rgN6HFlVEqnqIACLoCNALDtqL3DeX7+4M7o+nX+P5SFKgBriCB8JVCUKPpN+8rd37sn3AAscPkq"
                "3lIEp91oKLo1jUG05ByfqBgRNzxtEkHdhtNmnwo/+6UbQ24C7wP6VQDWiJqmfCXwBLaFTa9aH8d3Qp/noyIcuqb8xMGd4XeLTD9m"
                "fQy3fi7t1vqi9b7w0ZeW/K9v7mdv+OvaLutl78i0/HCjL7eOTvK9s0N44L1VANYIi2GtU7CF9H5ge9zyqhFdb8Dz/FRKp0MmMJHm"
                "nOzWFVdCWoDzUDroNHWxSJhxwgMg904Ox6Ej20JfxE6wdlQBmJUF1jIFBAnr4ui3j8Xh7RbH8w1ARdly0u0yMfzokW3B18rko0d3"
                "goqy64BQ74ILYCLRRDo2sL9IlYUBJSuUNaQKwDwd1rJINA63+ZX+jr1NHTBQ8PxV2gum5Txv7tcpT2yVz57eqD2fQJbD5LhSWuVC"
                "JoJdisJaUgVgQJusZV582+HeskU3DSbUuFIBqCiNnnDtAfvq6dHwHSq8C4jTo5GFQWHLCQsC1UagNW6djrKWqepYRvYPldiEyJVV"
                "SXLWX/sgv3JiS/w7bzkpEG/8kuGGB+vMDkViFYC17TF7hLWqxDOsg7U7i9v2JerclQ9AxQVhfMYNHt9a/JJafk4CjwULAgwsGDoN"
                "BQHRKgBrUkHJWpVLAUp7vY7VLA5QrrxKUpJuPmHedHq9/sc8AxNBAROg3oXcCd36Go1AdRvQslYZjKSarBvUIQxmmQJQEYX1Z21r"
                "ejj8QLehv+s8B1U4FweDiuAdqEA0VQDWlIyEtUrRVkq6w5ECgeVTSYLQ6PKPZ4f03n6Ng0Y5RzEBTIRmR7CRtaXaCVhnrRLsSEa2"
                "EyLLrzI6ZQamRvzmsxuiJKUoT1BMFEanBdAqAGuJw7FWBWLdYke4KirDC5bheXvtmQ1x0ERmeYIAa/L0vwqAqq7l313QaLlqKmlh"
                "XtnqmNelubybta8KAKKsXeqBPldJRan3ZOe60/b2ek/erVIFYM3LyVmr+qaYK0J5BK7MtWfl2a/hm4u4uZaMTo8GTJQqAGtdT9Zw"
                "AMhn+hQPKwFBuHyVPGN+scXMwALb04JnVM8FrCZHr/EkhfB0XlQFYO0IElmrolAW4k91ZJGWtrjcM4GKYWq4+6X793b+n1sfHP9n"
                "7Y5uSHMdMJGnsFFo9GXAlZKlheTVW4FXTMUAXvzMGZmMHg8Il6OSEXsnenL2Q//DKDfff0v2e5PjZgGUpxKSwmxISnO784anmzWk"
                "OgPY4bewVqkooqZ30B49sEU37XZqDEQuVcUz3Bm7fcvEht852Pir74r2db/84AuG3jlxYvbtex4J356WhgtJpO1KdjjPR1jbqgBM"
                "mGnWLsGLP3laJt7+Yn/zOzIaA5dzGVDxNPzwwKbFXa/5dPt9d9bOfOCj8yNfP1kfGvn5Xu3sofm2/amxKcs5iNJOcrYnJWtdFYCz"
                "Zoq1LKCLCfZPvuAe/PGXlre9NKUNdAHhmZlzE4FIRREcTT/cHMq3/VTXHHvYnv3kZHPh1gfVtX9heqjTFJUfHp411kQwSj31rEt8"
                "FYBqJ+AKsygGw8P24DtGdbixJ1x3a10zwAPKeXJuIJceBSWZpqRkQKTisdHVts3d9Pr9m+JeO//wbLFY+MXsto7z2Y+dGY/Oeb6r"
                "vWDbJuIsklmE1aBaBKxoS5vv/LT7wq9+yd3/hVx8x1NoIBDPTaCkJI+5dPunzcTZh8yBg2fN5JRiqAAoRh3rO5skLd3rLQPjU83T"
                "HG7fS3AWE/nh0+vje3u1WLqAAaTaCbiqVAbjwHu+4B6460v24e++zu/+hQ1xfCAlIRCZlwVO2bOHp2X2A7eEfb86oM3ZrvT/9YLM"
                "/lRb20CkAhDJisbL6lL+hSv1lG8OcHiHgip5pr/cXjBbR2fklc6bpqsuAda+Mu/wTBRAIBpAQDlPFIRzXyN4BwDWg4iQpHVAuJoM"
                "kheUZ6P031lQfNwTUouRQKSkDH363a70Jq3a4w+ZR3lEDv7nm2Vf7Rv9a/4JACig1X7/snZdK8hwLRe66RBz9Qxb9EB46MTG+NF+"
                "xiubXTagVQDWvJ03fCNPS0Ci4kpIc0hKkAhGQYHgoHRQpkq/Iaw7LRiF6XGhpz1OHPgYueZYNSQkuKSGqrKcFDAYDDJjMJ8Szv9j"
                "MFgsDksSYDKc5rA8dqqg+1sOXXc7t715gAH31X0XQQEY7Y6PnBg80phqz6PSwZ3poQO7cZrG6eH4V90GW9NSZ1n7qgBs2nUHT0vA"
                "eqXeVVoLQr0LxisuClEgz6BfU7otZWZEuLFncAH2XwML0sUu9KjNFoRmykQ8y/T0IYxNSCRFEFaMQGe8yYbkFl6kG1DDwVOBn52c"
                "6byuUTQGrVZXeCO9Teb4yGMbJ4fOmCy30c6exbf3IGrw1n+u05Rf7Htt8RWsugQQCF4xheK8QAATzgeg8ND3Sl4oZS70gsEG6Pc9"
                "6oTrt38DO6NlbmPKffJFZKFLamrMhCmCekQFEUHEcFUoEAJqlbmdQ2xvXMs1IRItNen7Idc7HWOpWOWrnostsrJxo/Nu3MXsDDbF"
                "9meI2QhiTG6D7reRZ1LdBagohe/Six3miynGs028fsv38/r2dzJkRkAE51KMcVw1RsA5jHUYHynKHr1y8e/nBvL+O7YsDAwm0QFK"
                "JWB9cmMtb+7LyhZZL6Vx5NPY/iyYhEtSBaCiKF49oHyrvJFX7vlebr39+7h2y8vp5XOUvo9qBITlYGKODg1g77iddTe/km5TmHUL"
                "zDR6xKLfWnekvBHFcE4lUvP1mwb6w9e1+8O088enN4qlTjTVTkvDJauoRhRliCEGshHSrMn40E5uv/Yt3Hbtm8lcg053kuBzRITn"
                "TcHFSBZLFtYPMHPtKC6pkdQGUANRA7mLY7bUVw7PGCfKBSqNsjmEMDrTnGC+McPcwDw6cy+mcwpNBi4vAtUaQKWkxEePLwN1m7Jp"
                "bB+CoR+7dGKHmc5Jzpx+gKZrc1kEpIyoek7vHiAxlvnxjN6Qw/VLvAEMqAhJqS8eWDD/0EUBlHMqBAb762n50xvODB+lXjRBBMl7"
                "pFMPoEEwta2gvgrA5aoIUSN52QWUTetuIgy1mDu1n/qZDifjKURBEC5GURRDDB5VT4w5kmUU69czs28AdRZbBEwIlAlPKNPIhpP2"
                "BevPmj2gXKgSycIgI73x24747M7Clh8VBDIHxVGY71FKDlrw9DZVAbgUFaH0PRb6XbawmRsGvoU/838KAmCeNQAGIY2DOM2ohRzd"
                "MEa4cS9prwO552kpjeE52Tk0b3g6lYJmf+Alw53xtx0a3f9RowYAUgE9CfNHAOHpvbIKwKWrCEI/dBlNarx0x3eRp6DCcyIsGQQQ"
                "kOneReNhor4iLcwtz7TxpxIYyIdZv7B52+MBwKjhPAfiWB5VACoCViwOkAiiPCtFWSKAQlQQnlEUttrAep5BJQIJw/3RG9Ytrv93"
                "0fp/H1EvVBzLqqICqpEtRy1lovRTsJFnIZwngHAx3bruSErZAMrFVGcBIyM3n7r9+7606VPvLW1xXxKSKBi0CsByq4zMCJOjSqcV"
                "ARCujGigPWc2NztkXEQlYGMm44ubt7fywX/eyRb/RWmKCW97iJoqAMurEiwsDEQm1nu8BVGuiDKBF0wl7WZXuJiKAJ4oga0ze77n"
                "xNCh959pH/+Lvut0jNoqAMuvYiJYL6BgIleCgLYaPRmwUXg2FcWoYcP8LuZrMz96duD4MVTuqc4AroqKyrkIBMEoKM+bAV6YFmbk"
                "Uu4AVAqumdpz+2x98sWPjT14T81bAFCQKgDLpRINNLuGLBcWmhFRnjeFDaI0uAQVJQ0tu31m1780UJbG/3Y0gV7SJRIBqQKwPCo2"
                "QFIKouC88DyJChtEqXOJKpGxxW2bouiPHxk5cCrzyZ+WpiRIQKoALJdKNGADtOcN/ZqiAqJcNhNoAwmXqBKxMWW4s2FPJ1v4mbOt"
                "E6eiiZ9UNLBcqgBUokBaCI2OcLLuUfP8AhCNdgHPZajk1PwAuyauv6Ww+a+fdad+JEi4XxBfBWDZVFQgWlAjBAsCoFyW4JhQoc9l"
                "qAhQIOq4/tSLXzJf+7uvy2u9wyaamSoAy6oKgA2wbsIwuS6SZyDK5dCY0FHBc5kqhmhKJmtnvTflXYjMgbLsqgBUbABvwRvFeUC4"
                "VKroGaD/1G3EynNRsQTp50dH9n9YNZ6u5fVYLQIuu4oCKtBcFIoRpdMEF0C5JFqmPOQdcwCLLd1/ZJv/A+PZsuOo/fZa34xdLAQV"
                "IUrBXDYz28kWft5EM+Oi5aqpAlBpdKHXMHQbSqemiHIptEiZyjNdAOjW9YH7byj/z7TP7o1nzCtqfca4iEpCN5nsHhs6eLdR8wkV"
                "JUqsAnD1VIKFrC8MzQpFGhEujXdCNFoEG1HB1HIhLUhFES6qogLztZmHzrSP/V/1srkyF05VACpFqgzNGrYed3jH5QhTI5GpUe0j"
                "Bp9yukwoQHkmFUvXTepMbeK+NGT3sFKqAFSch5lRWGzD2NmICpdEYMY7nc8TPTx2FibXyezsQOwMzQguCk+nkjHdnHj4zODJv7Ux"
                "QZAqACujIgreQq8OAUWFS3VXNJyKlg+6EjYdk9jLdKrbUNqLBlAuVBE6bpKZ2vT/Csb/jYsOZQVVAajYCB7otgxCQjCKhBITIyA8"
                "i7tVuCc4ZhMLI5PQa+ipPKNgkZQvU0mZHHhkZrE+84m6r88IwsqrAlARQQTs/FEauSPUB+k1M0yMmKBcxKQKiAfnYXFA8YkeiZYZ"
                "YD3nVASI9N0Cc82p/ze48ktpyLhsVQAqKlgV6iokF3wWVeiqUHJJDGiJOXMP684Mkm94IRNb1mF9oEwNKiB68d2FSQFFpuSpfsFb"
                "PXlhACpClKhHhx6Z6Lnuf7XR7Y/EKgDPS2WXCt+owu4LAjCrwl8Dn+RymJS8XmNwssO6U8cJWY2HXjCMtwYbFNFnWEdwkA8oAHmq"
                "719sxjdDvBWECoCgovnUwOk/7KXdKRstz10VgGqhzlEvUv1H3ukbgqWVZ9Sve8QNGpUhE6lxjoKPlu/pJ3FhZihOlIl+UoWf5RKZ"
                "CEYV1wvccF8HVyqH9tQ5uaVGlkdcGXmCKqqRKAqARMLEcDg+OmwYm3HVQiCWwvY4MfjYVLD+94yas1RwPK2KKEQD+dLp9Jt6df3a"
                "LcfNnm3H7M31nux0HmwU6n3hGV7HNdoSS60QRubsC5JS9uaZ3uWd/rEoi8/5qUEjmAADcx4blC1H+gxP5vRrwrFdbeqkGAWTZNg0"
                "IxIIKD3Tp7s7/UCnF185NtO5E4SvXgokFHb29OGR/f9BTTygokoFx1NURKFINUlKXr3rlL1zYNG+sT3PzeOTBsGwRDlPeTpGob1g"
                "YYExb/Utm07bl00P67480z9OCvn0pe74KxNhYNYzPBnotCBPIwfiMfKYkyQ1rEsRoKYZO8I2TmbHPn4kj3+2YWDLndlC4KuXpbQd"
                "ppqnH+umnd9PQqoCT21iFYBKsOAde7K+vGbrcfdPr33U7uVJB71yaRQAF2Dr8XTj0Fz4Z8c3hRui4aeA+y41TMEJPrHYGNj66CQf"
                "Dh9kSudJ1BI14rCMx1Hu4PUc4VPxsZr2bmm/hWyBVejLz56UK0c4L2G2fnzyyMijf+miLUSUp1MFoFKr9amr8JtbTtjXZeWVfrQ2"
                "MrAg7DxkX3N0a/gzFV4OnAIil0gFytTiQoNUAwkORbFYcbGZlIVp1Bi+cSTvv7F2tgPUAGU1USIqEUEQFUCuUFQUJYIAKqgUOtOY"
                "+POZ1tlfrpUNIpEnqQJQCYY0WH74az+e/NjAomyzgWWTFsK24277oW3l3Sp8E3CQKyfz+Dd1pPvTrwhfs01wjYTVuBvQ0XNzfrJ5"
                "2reKdq1Ztsh8E7BXIACe3C3Sc11qocbpwRNzpwePfSb1KU9SqQIgCmWimxLPr1z/+eRVQ3OyiWUmQJZjtx9zew/sKH+nTPgpUe7n"
                "MvQ0p8RjMZSUDGhr+GX+9p/ZGjfekNEABPCsPo5Obe6xYyP7f+P60y964P7Nn2zmtlhf87WGoholKk9HeEY2GlHBFDbvJj47u3Pi"
                "+gVVJJiyF0w4BMITKlUABOhnvLjRlZ/ZMGHfODRnBZSrpd4Xtp5IXuvT8Niptv6qKId5jhTFYPia9EYezo/TjX2MYXRIB99ynd99"
                "7uAPgLI6KaJmyKgd6tbmPzI3fIZF6ZDk9UQlXlYAXLQSRaWwednKBxFkadQgKjxJpQpA6fSORs+8fXzSvm5ofmVOk4fmDVuP6Xcs"
                "tMMjs2P8lssNz4UCgnCD3UHaMBzonmGuyAcatn5LRs0DDpTVK9LwzXWt/tAbH2k++qsnJrphsJHRSuul10AZA5d+BmBRUQBcSHh2"
                "FcNXKRV2J6X8xqbTK3fwL1HGpmX0msP2H7gi7rRlfgkhUha1z1irzvhQRpH0Z+Z975OLdLwSAWH1iqQhIy1rzf32UHz4xDSTkyXd"
                "0tMtPEYEEa64ShUAATYAf7b1hLuj2RVAWVnC2JR9+Y794Z3Z7ISVGAwiCZCdm9ozTAZk/TKkY2OJvXZ7ay4Q//IROTif01vlfY+4"
                "kDHcHWvXY31LPbFmYiHn/iOzHJ6cRxVCVK6oShWAYNih8J7dR5LrarmwWtR7wsbTck2ZxO8pbH6LN+WvRwn3RYl/P19UiV+6cP7+"
                "syjh80HCJ73xf9KV7muHGhm3jm+ePsap/T3ycnUHQEGF4Xx0ywvP3nGP9emuQgqcEfpl5JHjCzx4bI5eEailFmOEK6/ivrp297G7"
                "Pce/3XnEfU2tL6wmokp7wa5/4YMbfk7Lb5hJfborifVBUYNRQTCcgwJIJBKJElnf2XSDn71+b96Y/e4T7UOPGt87zWzsEmSQVU1J"
                "Yur25HuueS3xj+6Vz//spJn8m5rWyYtASeTYZIcT010GGynbxhp4VXyIqFKpAnAJq/11ra8/JW/Zfsx9R6sjrD6KUUlGZ1s7YHgH"
                "RCCwRC++k66UBJJ9sTO0Two3ud7rdFPrKXhWNwUgI+MF3HB7LaT//mP208lxc+p9g6aNRVjse3yI5GUkqhJV2ThcJ0sMPujFLxMq"
                "VQBUwDsYmJc37Dxkv3t02tRBWb3C0lyyAqMJG2b3joGMQQEEQFj9AgbH9WHf7ZT80j3Jvd1Z5j9oMFgjOGMpfODo2Q4IOCNkiSVL"
                "DM2awwelUgUAUZ6gAqJgAyhsufZh+y/XTZgbQJc9OEWiebAsAl6Umo0MpIUYlpUAEcg5T1g7PGC43l93Uy1m7/yr9O43dKX/xYiq"
                "AEaENBEAjk12KcrA+uE6O9a3EKFSBQBs0Ke8Iac1B60F3jU4x22w/Cv+/Szy6G5/z9nx+JcqnM1ybh2dsv/g2gNuV+IvHoFKBAxb"
                "46YtX1+89APvT++5pSO9MwmOC1kj1DPH9EJBjAvs2dwmRuVJKtVdgCgMecd/2nbCvrjZMwLK8hDyTHl4T/mlYLlNhe+PhncFo/8L"
                "Mb+Gqb3uEy8p3zA5Gu4D4WIqkYREdsTt6+/wL/jILX7fnm1hE4M6gMWS4J6YmkkocuHAsQ77H5+iVLLUYKs7BtUagHdQ78mNew6Y"
                "7x9YNAOiLBNhrh05stX/VRT9ReAzooqIw9g6npnuWe6ZmtSFg7v0a94G218AORdXyci4Ody05z7zxd/u2M6/TnD3CSAI52AEVKHb"
                "D6jCiakuZhayVmRX09KgTo0GDouifIWrAiBRAVCBNGfX6IT85PoJM8gyytPIxFj84OyQ/sLYBPcmHsQ0ML2TUExjyhzXnWfbnP1H"
                "rY7Zy3NQUQAa2uIa3fmN87pw4ixT/6fAQS6gF1wSAMz3SnxQGqVwouzguR8jjqZRmqZGabtYFb5CVQEwIQJQpOpGps3XbTkqb2SZ"
                "TYyGmanh+N8Tz715BlOjlkJmsbOPIN1DJAwmI92dt2+Z3fF/N4t2BgXPVaVgU9xOoP/mM2bqyBmZ/IUUwzOxRv73+AIem5zjEftZ"
                "Chu4wW9muFtjvvAYVb5CVQGIBgBU2NNeMF8/OucAZfkIU2P6V1Nj8dNZLnQaMDXawZ29F9OfRpNBQ8hutNG+p+GbmcEBgUtRWWRr"
                "3Nq+zd/82r/KPvhOUTkCCgjPRAQy68hwIHC8M8uxRRCEr2BVAPo1Q7AwMsnrRybNm0BZTsFEFlrcPTcoj6alxRY9hg5+AlP2UFsj"
                "mHJjM8++c/fUDeNG7WUd/BUFDOvj+O3Xlbv/63F78psieskHswoIX9GqAKiBIlVGZt320RmT8CTCEuVKmRyOdBrxbLAaPQY0JWoO"
                "4gnG4Mps92Bn7HuNJgKRi1NAn+Uevj6HGzh6/uugAQdMKSCcpzwzAfQiv0N8lt9Rnvz/M2ahJnA8cvk8QzpqXxhuvOUxe+RVBvNx"
                "i825BMJXvCoAtUUlhnhtc1F3u2AABeDMWGR6JLx9dMZsXDfhfuRKREAFnRqNJ2p95jadSghxlqL/EEE80SqF67eGO+u+dvPctRsh"
                "cFFDAq9K4UUZLEQ4G5a+Rp5snYUtDk55uCuHhyNLFIiAgTsctA3sSeDVNZgJ8N878DHPE25J4MUOZiJPaAgcDnAgwKiBoOf+/AjI"
                "0owKvKUFmy2c8HAqgAGmIyxGKID9EXoBbkrgjhRuT+HuHN7dB4TLo1gc43FkfG/Y+fMnzelvLSXkBuEJlSoArlTauby+1pMXAKhA"
                "L41MjIbfPXyN/20V+48fDwBXSq+u+5OShXrfIP0cNzlPTEYRhIVs7vaBfPCNzXIUWOTiFG5w8G8HoNDzAVDAAggosM7AiIMjBfQD"
                "PFwAwIsTeEkKGy3cfkEARiwsBngwvyAAEW5y8JNNCMITWgLv6sKRLvz/6rDVwRcCHPYwH2FeYSrAyx18WwPmdSlERmA+Lk3/XAAO"
                "BXhNAl+TwriBgwFQQLh8HotNbvO3vPxv0/mvm5X5v3aaLHJOpQoAZcrgugn7slbPrAfwTsPh7fH+4PixZldenRXyA1xB0TCRp/QC"
                "QpSIH1gE6RNMoJkPvKTVH7gNcp7VbIQPeThQwu4UthguqmVhnQMKQOFGB29rwE0ZT7GoUDc8yREPUwpfW+NJur2lz7++Bi+owXcA"
                "KHyhDx/M4Td78Mfdpd/xxRmMOZ5VVLDC86cYHKO6jqY2fmia2UcLii8IwjmV6lkAXjs8L3safUFFtduQY8d2yE8NTkXqHW6r9WUr"
                "V1C0dILF18oaR4dO8IG9v0Uamyxk87z+i9/TuPX4nRaUZyfwUAn/rQO/lIKwZCrAIQ+5AoBX2JVAL0KpLBH4gx78ZR/+TQt+YpAn"
                "GTawzQIKCGDgIyX8ty7cUQfDkvv68LE+jFoYMBAUjMBkhEcCfLiAIxEOe3hpvnS5IkA8971tC+ssJAIWMIAVMAKbrtTdGAU8W+KG"
                "O07J2e1TMvOFBEel2goMQL2QOwbnzaj1wlw7dh+8zt9lAx8emhOG5sympJQGV5BRjFGwKqBKlEgkEkxJqxxs1v0wEHl2AjMBPlDC"
                "ZOAJ9+TwvdPwxhl43fTjMwMvm4T/MA9z8cu+P8LHPU/hBGqGJ1PYH+B4AZElnynhwRL2WLgmASswXcLb5+Bts/DXJShLTgSY9uej"
                "9Hd9+OYp2HcGvncCfmsWPtiDPHJlKaDc6K9tjseRbYWUPKFSnQGkhexypbQAZgf5wpHt8RezQoqH9nl2HrADrUURUK4YpYHiSpMz"
                "3Bnn6x/5VoSMXrK4Zc/EDTsEBxQ8J1FgIsBncnh1HTKBIQCF6QA7LHxtAp8O8Bc5NIQnUWCBpxIg6FM/nI1wwMPmFAD+Zw4I/EwL"
                "rADAf+/C/9uDWS4gS5GaCjDqAKCjcOrcusWfBXh/CVtz2N6B3xmCQQGEKyVhQEYYeu0Q7U82aXyGShUAgFZHdtdyqc0OhVOHt4f/"
                "USR6qLSBxWZgx2M2q+WGK8kEGbGBGhpo9ZsMztwE4ihs/pLhztgeiFySUuGhAu6sQSawwcLrM7guwvc1YVxhoguPljD/NAfViPCE"
                "u7qwI1maTQlPoUBfgXNfX53CN2fwqhoA/G0X3tVbCgWGJ4kKkSUKFAodBRTWW9hp4RMlPFzA7zvoAAhXjqFJ4+YhBq9tUFsKQKUK"
                "wMCC2WYDdnJU754c1z9PS5Ay0lJhYNFkRrmikpJNrQUaWSmEIBTRgVisuFsE2XjJAfDAZITAko0Ovq8FqcDeFKY81HpPf2e7ZWCf"
                "OR+S/7QI39GAnQmsczxFrjATQQFV+NEmtAyUwOf78DMLcL8HhKeY16UBsMC+BN5YgyDwugQGBT49D97AH/ZAuMI80zL3+dNydn+T"
                "BudUqq3AdCbHQuzX4t1ZzjEQWguWIlfX7Entir4PQJFmh82n19OaG1Fq85b2XJ1oLNa6TTa6AS6JQAS6CsqSAQvXGkjkwk1xT0Nh"
                "p4MXOAA45uFuDy+OAGAUBgUWgHjBQXywBP2yuwSLAe7pw6kIKVAIT3EiwKkAAE7gjU14bR3WWUDgfV0QlhzXK7wVxzBpTnUesQf+"
                "2yPm4Kea2qBSBQCAkxvDX5aJBoX7Gx1wXsGAGmoqWK4gAYZnTPs9b9bsY6+E2z6S8I9+p0W/bvGhHLUxSUCf37LswwV8ug/bHbyi"
                "AQ+VcCYAwlOsM7DDAcADBThgKgAKGw18ewrvLqGj53+Ok6duRByy8LY2XOvg97rwwRJ6gHKeAyznDRnAnA/IKQ8KIFxZghL1k/bz"
                "/+uMTB5saoMER6W6C3AOPw38DPBFAGF5tRcFQaTTgDIVXHTYaHHRJUYNoDwvMwH+qAtvnYP/MgvdCC3DUylsdrAvg8UId/dg0Z+/"
                "xs8EtliwAAoACgRAgF6Edy/Cr8/C5/owYOAbmvCOEXh7CzbwZHUDdXnyPoYzHooICZByhSmQ4vG8P/nQF+bM4q8kJPupVGcAX2ZC"
                "FEQhWPDmiX8XloGLwq2f13026l07HqWrxmHVgOJE5XJvc4OyJABzCkc8/GoXbk3gcHhq2uoCtySQCgjw/W14dQt2WUBAFRoGzJd9"
                "zwYLIhAivD+Hu3rwvgK+p4C3tmGjg3/cgiED/24BTisoMCowcsF6w5914L055Ao7LWz+sucBkOeRYwVadGWKT7jPfHRGZn9CVT8v"
                "iFKpAvB0VMBESAsBQIU8CoHnRZ72gZxNJ+J13sbxkbMcQSw2GgAjl7PeYIFhAcuSCCQCCByNcKrgqRRudvBiBwCJwE0p3MR5GbDD"
                "gfuyz8YMCKDA2Qgn/34KOBPgFXXYk8CohdfW4D1dOOshAE2zNACBpY1IH80BBWPhJgse2Gjg5Smc0HP/Xbg0BmgwJafK+5Iv/sVx"
                "c/r36rF2r8dTqS4BnpYt4ex45JE9nqNbwv+ew1tDMdeOOSiXa2Y4fObseHi0X1PlAtHo1ii6WaLigiIIooIgXBqFmsCuBBKWNAQG"
                "hCUCJUvzJArfWIPrEygVDpTw7g785jy8vwfdCHWBG1MwwhNSgbY5H42aOR+5hyM8WkJQAOgq1OTJTxkOWQDoKdwXWGIhKnyhhCHg"
                "h+rw2214Q3aJMRTAUJBz0hw/fG/y6d972B58+4A27+JiKlUAskI4dE3g716V85GXLs1dr8o5uTH0eR7uv97/xidfXP78yQ3xiyo8"
                "Ic11Z63Hlmgt3YZDiSgBvZyHXzKBve78qv8mC3sSLmqvg2+ow6iDboT3duC7Z+CfzcCvzcPDBSCwwcGQOZ/8usBmCwA1A1stpBf8"
                "HsdL6CoATEZ4wIMClqXfaZ0FBSY8jAMNAw2gZWCLg39Ygx9vw7iDU4FLoSg5fT8r88c/kH7g3z9kD/74iA4+rCiVKgDP6fQ/KQXn"
                "lyYrhDzVIqLPY4+BfOfj8+F+qr8w34osUYbmZYfTZOuxPaM88uKdROewUbj0SwA9f78/EQAYMbDR8vQUrMBvD8HXZOf3AlybQmIA"
                "C9MRToTzB/xrExg0QISWhb3J+SC8IYUXJQCgCpMRCgWAQx4eCxCBLRZucOev/+civCGBbz83P5DCf2zBLwzBiIUHSjjiLyGGjo4s"
                "8kX30LEo4WvqWn9XgkNRnlWlWgNISuHlH0150ecSTASAaGBgkdmZ4cjozOU9mNJc5IWzQ+w+eo2+v9eKv/Oiz5kfAxiZMdJeMMMn"
                "thl8YogSUYnESzoDUNjh4EdqMGR5QtMuPZn3p134YoTIOQrrDfyLJtyZnc+4FXhxBq928IESBEhY4gTeUIP/L4fcwDcmYAxPuLMG"
                "Ly3gE3OAgwhYlkxEUJa8PIVdF6w33JDCTw9D0PM/pylPXiOIXAJDic9PmDOPzMrC7LwseoM8EQAFFKXEk1M8OQyVKgBFCmkh1HsC"
                "whKFxZYe6rSYGJ1h/HLeEtTsyAaJcVuvwT1To/Kfv3Bj2b/pQfcTNhiaHW6u9cO+rO8fingQH1Qiz53CzQn8yAAYnmybgW+twYM9"
                "KJQnpALbDXQCuAta0xb4pw34xAI0DGywAGCBO2owtAB7LfxoiydpGPihBnwhh7s9JMITAkAAI0tbkncnACDnT/2f0ZCBmnApFLSg"
                "7HuZT1raRLRJQoJRQ4JgMeyMW9nEOgxCpQoAAN26og3l6fQzvWt02nwd8EbOmRj19y+0dHpo3lwzMmO2cxFDc8bW8jgcJVIkHDy6"
                "Lf6CUfr7Hkl+dGSaV4xPhDc0F+NDqoFoygCRS1ICB0uYV5hTOBTgTITpACef5o+bUfjvPbi7hJYBYYkAFuhHuK0Ge9Mnbxf+P1qw"
                "4OHeAo5FmFdQlnQilAIKTAcILHlFBj/YhhDhsIf/0gGvPK0RgestlIADPlfAY4FLJBaTGoQBbQKgRJQlDlgXx7BqUJQllSoADeWZ"
                "9Gv6QLehnwkmvtFGAeDQdv+hQ9vDH193IH3TyIz9V6A8k2bf0uqGbag2JMZuEmThoWvDzzZ6Zri9wFvb8/rCoB5v+3jtdaIJCkZ4"
                "TgQ+X8JPzp57si7CI4HzBBDOE1hU+EAB5Dytmx18Sx2swGQ4f0r/lhr8eQd+cgY+FwB96s+xAh8/93jwywy8JFuaYwX818XHpwez"
                "gadSMHbp8qKvkAIHIxy+tAVRRX1JOWsxMRCeuZjCeZUqADbwjLIcunWdnG1rHJ0VA5CUsqnZkQeTguFo+FcmclFZX25odGVfWshn"
                "g4VWR3j4uvAbw7OaSDScHfaydWpBY1w446XIQWo8JwKnIrwvXuL6rDzzy0O/rwGpwnsW4TEPucKAgbbA/R6m5Jl/RgA+5uGdXWgC"
                "16QAUAp8VwPOKPxRDwrhKSLw157LJwSJiwuyeL/FeUF4TipVAEanDc9EBYLVk5Pj8cTorNkKYGDdhrN2LO1Rnlzn2XLacjGirHMF"
                "G9IcABZb4CKHFpv8+yKTQVtos7T5opf+RDBhEaTGihB4ewdcBwIQv2xDXgAK5eIE/qgPf9oHKwCggCr0gEJYHgbQ+UXT+4TDls85"
                "AJUqACZyUdHIh4tU/0Oe6e9luZCWMrbQ0uHTm/RYe5GHt5zmOi6i3mFfWnJjp6XvMxFUQILE4DgeDKeMKHlaUGr+UDDxDMgYK6Wj"
                "gD7DYqfwnOS6NE8hLA9LV+Y4bI5PROJnAlIKz1GlCoCKcDE2MNuv8fGjW8LUnoNuNM3ZWu/L1jLhA90GvzI3EH9/oCOYKDyVMjpr"
                "G7NTet3DY560FFBwCgCiBIA8KcglvzfYcBS4gRUlV+DAFa4OBRrMycniUfvY59ra6gjCpahULwW9KBPBOyZnhvXX+jX9pdFp0yqT"
                "OD41or0y0T89uCN+1y0PJF8HGJ5GLTeMzJoban25/fH5lAJJgCJTYt2As5SupJTyWDfpnAjSx6oASuXi234hZU4m2W8P3bUovXcP"
                "aJNLUqkCUDqenXAa+I9HtobX7jloX3Z6Q9wyMR6Ses/kZzbwc9MndfvItOy1kaeV5bJveEZ+QFQ+BSAKwUFSeNKFLi5vkKDktjvd"
                "SWZoF6NA4MtVDACegkJK+jD3kLv/wUP22O80tP7xSOSSVKoAzLYjz0YAFczEKD/YXpD3R8OtLrBZ0MPOyyce2Fe+56YHkh8cmbGj"
                "osqXq/VotefkurMbsQgBhegsQ2dmWX/gCNFtBaA0RXcxnaddjPFUlUiIkeBnZd4ftsdmvmAfeU9Tsl9r68DReToIwiWpVM8CyHMY"
                "AFGiDTz26N74H0+vj590pQwrS5yXXz6+0X9gbiAAwpMp9dyw9bTb5R1vUaEJgApqIv2kT+56S5N0F4MtczBcqCJAxmfrn//YB1v3"
                "vDHTbB9wh0F+DuQ4lSoAV4MoIc/4E+94J8pjF3w+G438/ORIeNfs4FMjIAqNrlm/8aT5CVeSKoooBAn0a1362dL0su5k6YqzIFyo"
                "UmNq46MPHR1/9L/0NP9bQY4KclyQGYFIpQrA1WIic6KcAOa4gA3s945fnBoOvz8x6p8SAedxO47YF0rklaWljgqBgoXsDIu1uf89"
                "C7XZT5UuvxccFQBBRXW6fqI/OXr0/8rrnfeZ4KLFsupUawAV53m0dPyLkxuDiVZeNjZldtkAAKLQ6ggjU/LjjPJQdPpwdHV8az2h"
                "OAMCeVI81E0WP16azpuTSAVBUSYbx4vYcx/emG9eSG2Lnusg0aAiqAiooICywqoAVFxgrlB56xdvKN963X73trFJsy8tpG0jAOw6"
                "7F5lJbxqcswfFTfWdQOvJJ/7IFLMYXD0XOfwRPNIuWnhmgQAlK9eCkAW6llnLgxtkga0IscbBykWhcQoRgKiHocirBJVACr1vvzB"
                "/Tf6PxmYk5/fs9/+8w2T1p77nKSUn4yik2j5PwGyoVeTnb4P25mmdDI13Tr76OMBuIEKoiLt/kh2eP3+ZLo+gYspAAzDIAoUAAyy"
                "ulQBqGg0dJznl09uDH94YG/4+o2nzL/beNq0dj5md7hSfmz/bj9d75u7FEugQ7ALFEkyXQvZQTA3QKwCANRChmBskIAlggDwZW9Q"
                "ElaVKgAVUTCRySJlcnZQjw7O6oOi0j4zHt/SbcRvbi3w7bOD4S6jAd18Hen0o0jvxCFvWu8sTPeNacz46qaAkPkB0pBtNhhjsRFl"
                "7agCUDERnGfWRt5vA8wMxwfPjIf7TNRTRRKdUXxobaQ2P0OzN9cxYj9zqn10ZvP8NUMuZgKRr2ZGM2y0GySamkTTZa2qAlBRgbTk"
                "S/2a/v2QFJICED1KQKLFp744OXT4PRsWt36ni6ZZXQpERKVu1NSMrv0AVAGoYCLYAECBQFJ4Aj0WarMUmZly0f7f3pTfmEGTCoKp"
                "WVxiMHxFqQJQidax7sDDbDnRolO7jsfqD5So+8JU48xC5mu4WAMCX70UwdRETSpqWbOqAFRSX8NpBFsSEnC+ZNPDh7DdBaIZY6A/"
                "wtapPeQ2L2ezqdMjbnxfq6hz9QjgAAvEcxMAZSWJUhclFWWtqAJQUQwpiAMDRuDhDZ9j1i0gk4YsUZJcaMwJpQPvlKxvaeRtYjoX"
                "p1qn/3hjZ9uuVrFuG3iWn+DFM9k8dmimcfYzzXzwG9r94cGBYhCrbmUjoKQoDmW1qAJQETApIoJBMAoABhBRxFh69hSmO4mZT5hH"
                "mRp5AA0dknlHQsTFlGj34K3epoSbggmmsHnXu6KTxHSbjZarJ2O6dmry0dH739mpz/2Pkc76j020Tt25d/LGrxvIx4ehZMWopII4"
                "QVh5VQAqYkAD5GcJJeQIYgEgVwilYnsZnfggtr8fyWtMW3A+AwbAKioRDYmJEq9tFq1fqpetr8t8jaZp4bBT6xa2tJt5OwHP1VCa"
                "nDPN4389n8784UDZfsyoeXi6depwf3bXTQO5GWYFCdIwajOjllWgCkDFQDEFZz9MX5WeEUhZEkHmwcwrBgtuCADLOSjnoMKYUfMn"
                "10xfd2PqB4CS0d4GgFEAiEBgeQkAp5oH/Hw6+94s1B8DxZsireetO110Y6CsJIM0RaUmKqysShUAmyGdQ8jUp1AREHnKi3RVnv2v"
                "EQsSJI31a3dMXb8t9XWghBV7rs0x3Tj7vk4690ijHKDhG6ioeFOuN2oarDCJJhFvrYmGK6ZSBUBtjUtjUJfiNKXeTcA1uFzelBuS"
                "kL0p81kdBIhcfUIQz5nGsaLjFt+hwoHUZwz2R/Hipe+6m0RtBsrKUay6oUSTptWEK6ZSBSCdvI9LYVQQMZhiAXUJaiKXQyWS+HR8"
                "dHH9WwALkZXhEHx5dPDAB3OXf86GtJ8nfaaTM6BSjC6uW5/5zEBkJVl1Y4mmA48PV0ylCoCbeYBLoaIYBTWWfpaAKpfD2zIdLtfd"
                "uHFuxxbBsDKEKCWz2cxsJ1n4bRWdN2LoJx0WsmmT+GTTrqnrBtNQZ8UDEO1gGtKGiwlXTKUKgJUBLpkACngum6I7ar75zQPFOqC/"
                "Ytf9PTdTHm0f/LyL7n1RFE1LjIWkTOsuJq9qFYMNIQFKVpILSS0NaXpFA1CpAtDqDbESvClvqufNV4Bn5Rh6bvHImYGj70xi5hR8"
                "Ehw2pASJAy4mL1E0A2VlKYmmJvP1mlXHFVOpAjDdnORqC8Yz0B0ebvUGN4CyMgQwHB187OhfXPv/vLdRtnzXdXnFsW/gpokX000W"
                "WjYmN4uadDUEII0pLT+QJCHjigWpUgWgcH2utjzps2numu2jvW0ruPiX0HXTxWNDj95/qnWiUy8bTNenuP3UyxnIB4kSMxvtFlFx"
                "rDilWbaYbJ6WycYZXHSsZuu5vQrAWtHuDXO1dcPiS9v99ivS0AQ6rJQzraMf7mQLf3TbqZdh1TLYG+H6iVuwIaFRtKyibcCw4pS6"
                "H8Sbcvj0wHHJfE25EipVAFxwXE0qylBn9PW1onkblKwMQ27nOdM6+SGH+8wLzr4ERdkzvQ8XLVOt07iYSKs/2DAYQFlpojVqZWN7"
                "4tN1qc/OcCVUqgBMtc5yNQVTsm1q76ZWMZhBZGUYpupnQ89152tlHS8eNYED676ExeBNSas/lKxb3LyKtt5GRM1W55O9j8+VCUCl"
                "CoBRw9UUENr9oVazaLFyARAW0/mTzruzm2e2E22k05pGJQKCSCDztXXt3ogYtUBk5Sk22vHU1zYnIeOKqFQBaBYDXEWmn3Rf3ywH"
                "roUMKFgZll7S/dB8bfZztVBHUQSDqHAuioNW7XVprAEKKCtPMWoGk5iMXbFFwEoVgMLmXA0KCKKDndHvrBfNXawIQYnkdp5e0rm7"
                "cPlhFcUgNMsGTwhm3Pn0RhBAWS2M2nbqa8MN3+SKqFQB6Ls+V4NKRNSanYv7bqmXzRp4VoYy2ThZ2GCPjHbXe6MGAawYzsFKuT7x"
                "tetBWT0iWag1XUzG5tM5DMLzVqkCYKPlalARY9RuGumNN5NYBwIrQtDp2tQpG5JiuGyiogCEpOAcnEmG0pBew6oSGSjaJgvZ2NGh"
                "AyQx4XmrVAGo+xpXQ5TYMGpfXfP1BpgVCoCgoKXJj3aTxY5Vh6JYtQyUbQyCAtH4RuqzYVYVpe5bDBUjg1Zt4mJS8nxVqgAM9Iav"
                "VgCGBN4sKgOgrCD1tjzjbdHTGIkSkZgyUA5gokFFiRLrNd9IQQFldYhAjXrZ3JqF2ivSkN0NRJ6PShWAxdrc1Tj4SXxmN85vfYld"
                "4ZdrCKKlKx7Jk3zOxUCUgJSGZj6Iiw5FKWxhDYbVR3HRbWoUrVclMfkgz1ulWgRMeiw3b8t0MCQ3bZy/ZtzGBIislChBC5N/trD5"
                "dJSAosRkkYPrHsCooTQFQ70xts3sZvWJWHXDrWLoxrqvCwoIl69SBSArayw3E83mmm+8sVEOAWGFAiAogcVkvixs/6FS8iKKR0QI"
                "CRxr70eB3PXYOXl9du3Zm1mNXExtzdfHu0knqiiiPA+Vag0gH2S5labcViubd4Jn5QhBPHPpbL9eNuZNNNhoCYknzzpkZR0AUaj5"
                "ettoAkRWl0gaMuq+0T449mAaJfRFDZetUgUg8SnLSQFjbCPztTFWlBBMoDR5b9vcbgNgo2O+Mc3R7BFsdOffVOyzJmRAb/UFINZY"
                "11s/6EKyJxh5wKiJXK5KFYCJ9mmWU7Cege5wY+Pc9lFW9KJVUInaT/I5UYIgmOgoTUkSM0w0ACTRr7dq14Oy+iggJCFtNYvWtwTj"
                "Txg101yuShWA0hUsp9zmjIaNG0a7mwwAKCtF0Vja/iIqKghiSoLxOJ9iVAAIJmyW6Lawihm1zXZ/6PU2uj82aqcRLk+lCkBaZiwn"
                "he2NsnFbEptAn5WkosHbcuFcAECFKBEXHKICgBU3YqIZYdWKWHXJSG/9jWeax9PC5Zf/RGelCkCr32Y5pb74mqys3wnKKhCDhB5I"
                "FAQEQElCAggAMYQhq3YYdPUGIFpG+mPN/aP312br0yQh4TJVqgAMsZxKU1xTK+s7IbKyBAUUVS4gKiShzjkoMurUjYKyWglCsxwg"
                "C7W9qc8eSC53W3ClCkCtrLOcnEmaSUgFlNVGUYxakpigKABKrJtg66xqglNHo2x+W2Hy+11MHuJyVKoAHB95bDl3ALJufnNSn28B"
                "kVVCuZCCUfNEAEw0NVGpgbLaDfXGvnE2nf6D+WzuIauWS1apAtBLOyyX3PWz7X7vuoYfAQIrSxHEWDU1VEQQFCVRhwvpEwFAqZno"
                "HKuaArBxcevQmdaJ0Wk3SRYyLlmlCkDqM5aLSryp5hu7jWZAh1XAuOiaqJhzAcCpI/XZEwGwxmQuOtaClh9loBy8PQu1u7NQP8Wl"
                "qlQBqBdNlouN7uU22l3gWQ2MinEhGzDRGMGgqjgc7oI1AIMkVi2grH6Ghm++pp0PfagWGn8OyiWqVHcBBlkupS2uT3y6SnbVKaLG"
                "ZGV9KBovKoCAiUuLgBEFIChW1KyRAERqZX17K2/vNGoQLlGlCsBgb2Q5dxluSHxmV81rtdWShaz+6Ogj0nd9ovGMdzYxfuaFeFMi"
                "gDfWrJ0FNc94d2O9ky5uOt56jERTLkmlCsDhdQ+zHKKJbJ/Y26j7BqsmANHRLoeaKrHlbYGNlunmGT65529AlcLm7Jq4wew5e9Pa"
                "OQPwg9IomreXtrjTBPNRVl4VgOqNQEqwIU1CVktixqq5BMDSKtouCdmoDX2SkJFnXaYHTmHU0Eu6bJ3ZbZOQsnYYslC7pZkPvq7h"
                "W5cWgEoVABsSrjw1qNm09AJQB5SsFi46RO24UetEjU98xkB/CFHBhZRm3k6FFAisDYFa2RwY7o/d2HddBOE5q1QBcCHlytNENNzk"
                "YtICw2qiophotpnoBkw0MzakJHkbFGxIpFm0apACXdaGQNO3GCyGN5xqHRmz6qYFIs9FpQpA5uvL0xXjXyRIG5TVRUwSk+sfn0EX"
                "0xk1JV5KQEDUqagDZe2IuNhgqD9yjY3uBwX5LaDDc1GpAiBRWAZGMC1BLCirjEi0Ayaa9PHBK+Q2R1TIXb8MEgoQ1pZIGrKxsd6G"
                "bz/RPvp7pSk6Rg3PqlIFIA3p8nRFwwZRyViFrNoRpy516iB6bHTn1gASjBrPmhNJY2Y2LW695tjg4TRKxGBQnlWlWgNIWAYmRjMi"
                "ahJWIad2xIUke3yIrkSJgKAo3pQCnrUlYtQxlI80mkXrrTP1yXcUpj8parioShUAEy3LQqgDhtVHTHRtE5PExYQCIU96mGgokj79"
                "pBegBARQ1hIXk2Tb3M4fX8hm/2Y+m5l0MeGiKlUABGEZiCAOEFBWGUlCOphJSJOQEosG7f4QqCHzOSaaXmlyklhbYwFQQMz2+T0b"
                "jw8eurmbLD6YhqzHCqkCUFFWHUUQaqE+JphMFBq9dWxZuAYFBPDifSddYKhfZ21RBMFpxmhv/Q8peiiJ6Ye4uEoVAGF5iACyGhsw"
                "3B9NHh67L51uTmBjQs3X2Dq/ExMthc37WagDBgisPcpA3n5hkLDbBXfxAFSqAHhTsgw0SlhE8CDpajsDaOfDIAz2XAcXU4IpWcjm"
                "MGoobD7V9K0eSJ01San7ZhpzHbZquKhKFYDS5SyDGEw4E4k5kLJqWMAwn01RmtJbddhoERW62QKC0Hf9h0b6Y4+CuYVVTS4Yc8Fn"
                "Cb2k05mtT5591kXAShWAPOlx5akPJnxRRb8BzABXhQUCIIDlqQxKwWz9zNzZxqkPFTZ/0KhBAIzSSxcByJP+5/qu9zGIKxgAAewz"
                "3IkQQFFKSlvgxROMJxK9mtgrbTg00Tz9gbnazL0uOi6qUgWgsH2uPC2CCR8KpvwB0I1cBYXrFi4kU1FCmbs8NdFwDoIld51wqnl8"
                "frJx5u7R3roft+pUARHBGCjoA+BNfrKTLXym72ap+ZV4makQxVPa7lyQMG/UNC6ogCoSo/Fh0S0WUULoJIvznXR+Njd5p0z6p6Yb"
                "Z9/VLAY/WisbqERWQBWA6jageFG9r5MszgxJH1G3jAeSQcXH+zfe+6nrzr7gn05nkwc+u+njN9V8vQQwiK35Ol9c9+nTRwb3n/yO"
                "L70tihp9ptuhNjoWs9mZU+1j8zumr29f/f0Ajpn6aR4cu++/PB6r32gVg68BVaAEChWd97Y4rcQT1595UZmGTPvR4QiqMdE0ZME8"
                "1zcaVaoA1HyT5aHx2OiBj7XKgRcOdbfXoQsoV44ABnCIOtNPun/12W0feTRGXTRq7vWmVACDiDcJhc197vo8F0bt3cGEt81lk+8e"
                "zMcAA/irFALB2yLkSXemMMWEN/69oIAqEFU0eFOWivK8VaoAWLUsl8IW7zg88mhjswk/Nr64BUi4MgzQo5PMMt+YLmbqU/8jd/0/"
                "7ae9LsFgfeIFBcAgGDVYtdjouJAoKEIU4QlqyV0+f2Lo8HsmWqd+duP8lh8f7o6vG+yPAg3AAwVXngAJ0KSXdh4MafG5Qd9GVDoX"
                "noUoilHDFQlApQqAosv5oNGBxWzuPx8deejkXH1ii40uMWp4vqKo5K5XilIGE44cGTnwl1btgcSnRFU88XnsWLIUtqSbTBWi/KJV"
                "Od0omvsmG8WmXta9udVvbx/ubWw++dJAn+e+CwN4Zusni8Va76NnB078vsV82mlGjqdSBWDNxqXuGwe76cIvPX6QEo3HhgTB8Hx4"
                "W6AmsHl6FxvmtpH5GsF4rgxFVHDRYaLRJKT/LfN1Tg4eqR8cf+Dbxue3fPO1E/JKG5OWoA4VK4gFRFTM0xRBAFVRBRQ0KiiiQVGP"
                "EBWj3vb7j408eN/E4MmfMcF+thbqBCJrXhWAKgJGLZmvoxLOBUB4Pnx0SzGJDkWvSsiSkPaSmP75QmP6+Jc2fupo6rO9NrrBx6fx"
                "+NRFTWqiSQR5UgAUFQSNEn0kFip/P1oG63tR/EI0sauiIUqcyZPuR5KQPmqiQdH/fzt1UAQACMMArMO/5yKCD3dLRCR/YtpmJ+Dk"
                "BSAAQACAAAABAAIABAAIABAAIABAAIAAAAEAAgAEAAgAEAAgAEAAgAAAAQACAAQACAAQACAAQACAAIALbr9pUzc/FtwAAAAASUVO"
                "RK5CYII=")

FAKE_HOUSE = str("iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAABMl0lEQVR4Xuzde4xc133Y8e859zF3Hjuzs0/u8i1aokmKlCw5imx"
                 "XlWs0aeokDtD4oaSpg7qAakcwnMJwUPiB1AHSoP4jqG2oqOsEjl27iu22cYIiBtI2jeu6qdK4qeL6JUuiSIoUyV3uzM773nvO+d"
                 "UoasSinhTE5Qz1+wALLOYCAyyw5zs//DB3xogIL09KKcvVopTSACilNABKKQ2AUkoDoJTSACilNABKKQ2AUkoDoJTSACilNABKK"
                 "Q2AUkoDoJTSACilNABKKQ2AUkoDoJTSACilNABKKQ2AUkoDoJTSACilNABKKQ2AUirmGvnanZ/gehWFmLSsUB81mVSGtAaLnG8W"
                 "bFcL9lxaouoyzq88SkwPiPgBMcL81gppWWWU9Wn1FukvdvFRk9BtcHH1MTLZQoi4nBhh9/mD9OtdfOSojetsNnMcK8wVKabucCU"
                 "UBeRVR2NUSXv1/MBKt/Hu+V799u/tu3D/wXOLv7fRHoxb/apsLAxZ9Rmd6oRJCS72VFzEcllhszYmHaZcXOwzv12juzZgbVDn0W"
                 "qfA+fadOYmZMYS1z1d8UzwlKlnvlPjxNllzq1t09io8/hal9XNOU6tb3FTr8WgWmAuVRjXSkIETgK+4Wj7hJOtAbvPNckzR5Ynd"
                 "NojmkXGxfYQe9Kza9hglJb0sglPLHRw1mPE8HwmruRVu/bzt4/cAcWEq+LDyxqAa0+JEbyVLC2jQ1bMP/jRbx54R2tQa4Fh34X2"
                 "a87s6nwlLaOPBiN/LEa2mS5KA6AHGAKIRczTr4kJi8GGnphQXn4tRKGWjpObpJS/e/T0+r2tQaMJAQgA2GDYf2757t0XW3c/tn7"
                 "pD6t58nGfhgeDlQ4YrimlAVBC7FKiMIeLHIkPIBEYQMBHfiWbNO4XeGiSjf6Dt+4xb32vtL6ajLKbo4G95+Cp1Xsb3UYDBHA8lQ"
                 "CO2EXcdHrtjUWav/H0oc0vVr18clCd/E+MdLk2lAZABeupjxZJyz2MqpdoOk8Rj5DgwEA6rP7k7idverPBvHlY77xns33233ryP"
                 "3Gmfvvec8v3LvaarWc++DxjCNIi4RXf3vOWYTZ+Czdc+PSwkn9mUi0fFJcO2XlKA6DEBILNSSdzmFpKf/7/wLiHRIZDJ2/9cYwE"
                 "JNj6cGHp+z/v3GPzd0YhAixQcmUCEKhPKtz2rQO/2Jnrv/nMeudzaSKfL1L3X5NR4ph5yjKTNARiSur9JSjWKGxCfdQ8agQLASi"
                 "AgihEgACOF88DJe1+o37iu/vuXXti8QvrT7Y/aoO5O08d14DSCUCJddR7a2zODakO6z9bG83vg8BTBV46DjDUu7XFI93aL23O93"
                 "86LZJ/12mOvlCk7k/ZGUonAGUEfBwY1kdvOHi++VsnHr75o5WyOg/C1SWABwJL3ebeW7+755ePPrb2Ozc9svLPioo7XiQeI1wNS"
                 "icAZQBvA+NK8YZDZ1d/sTao3T3fqe83RIBj5wjgAMPqpeZNK53Gr1za6L8xXez+fr8++W0fhZN4y5VTOgHotv/HfOTe5iNXe+rj"
                 "wrCSv351q/3AiUdu+J21s8tvb3fm9hsAHNeGAB4TYOl86+Zbv7Pn/ce/t/6lXRvNfzKulashEp6N0glAF3l4jFjE/NVjS5u7P9z"
                 "s7zo8zrrv3W5t/J6P/BeL1O1q9xbfc+O5tdfVxtlaFCwQAM90EMATe2uWOo0TzUH1SH+j9XeePNB54ML6pfslNz2UBkABgI88c9"
                 "01kDUmcxeoOocYg4/8rc3+0uFKni1U8pWFxrB93F0a3ycmTtJRdSUKBhDAM50CAGlpk8XN5vFmr3Hj0qn5e759w4VPntrd+aQYc"
                 "pQGQAnWJ3gCc509jCo5NZmQuvCayKdV8IAQuziLXXM3AAgQmA0CCElhsl0brROLnbmP3Hiq+/cfX+t+3Ft5ADQEugPQCIARTLAE"
                 "A6ZYSNq9Pa+Lgs0AnnroAyDMHgECiTPVPecXb7vzoQOfaIzSrwJvBapiePnSACgxghipRT56nQ32c3NbS282wRgQri8CeOJg0oX"
                 "zrR951YP7P5+Nky+nLvoZMVIXI1xvdAegB/s5rwcbWkkZHzdi7zt28oa3VvLMggeE65cAQhwiDp5dunvPxfm7H963+Qe1SfrxYM"
                 "OfiZWe4WVBA2CNYTYJctnvctn1yqR+V+oqm8GGM8GGAQBAsAEf+XYtrxwPxrzrwBNr92RFHfCA4+VDAE9SWo49uvamQ0+033Tq8"
                 "MZnnfCJcRQeCkb6YLiOaQC2C8fsEYxYEokxGACSCCpYBIMALi5ahx4//pmkqM1tLZz9XevtH/jIf0OM5M1h/bb6uPqOtYsr92Tj"
                 "hgEPlLx8CeDI8pTDf7n3F0bZ5Oce3bv125Exn+k287/AMeL6pAH41taQWSMIFUlYKhaIJQIs7UbMfKVGIMeIx4bWT9SHC4uxy+Z"
                 "qZ1v3lenoXZcWnvyj9bHtrG6uvjXLaxEIUKCeeudhbZJGx7+3fu92Y/Tzj+7f+tQgzT+/NZ//WZjEJdcXDUBiDbNGgFgMUSRYEQ"
                 "yBQEI3TYlsl4QxyxcPvsaEqAolICRF1e46/4qfAAEEKHluGoLWoNq47Zt73r05P7jntN/6HM3yi5OK++9TuCzUm4GUYCVgfJ1xb"
                 "KiN545Gwcb8AA4oAAc4XgjlAc9St7F821/u/eWDDy//m8OPLf2GFfvqIvVMFQ2ACpFnHCdprb/77Y1B+1YQQHgqQV35fgAC7YvN"
                 "/a/58/3/+PBjy5/Z+0Tr11wcbi4TzzWlAVDBBMZpbhvD2tte8cT6A0ceO/bx6mRuGQIvNQ0BLF9qHDn6vdUPHX145XMHT7d/dVJ"
                 "xB10Sdr6tugNQpXXMl3NvuunJ/ffuGq/cWZ1UFgHAczWoAEAUDCubjRPtbvX41sXRTz+8b+OBU9mlf2FGjNkJGgBV2DJeKtrve+"
                 "2lV79nrqyuguzY23WVAELirFk937y9uVU9urxYe/2Zxc57DTzM1aQ7AOWMj5bz9n13bdzxwbmyvgqea/EOPiWAp1rE1cPn137q0"
                 "IXlT4/j8hauFg2A8ibQKhuvf92lV/16zddqkF/zg68CRoQDmyt3nnhi98fypLyR6ac7gJrLmCWCkEiyenv32Ifrrl2HEWCYBipg"
                 "BfZdWrrrQqv3/nPz3XcZMROmlwbAYJglYsQ2i/rPHOnf+FrIp/Lw6yQQm+On9/7CuVb3K99Zu/Dp1MXyQu5JiW2kAdhpE3JmhSC"
                 "kIVm6tXf43YbYwHgqA6Ac1bIaHz23/vfOtbb/8zh2Z6JgeDa5L3nl4i5+7PBtUEw0ADspEGYpAKbuqm84ONp387S/+ivH/s3Fv7"
                 "G+1br7kZXNz8YhQngqAwQREmKa1RqEwA7TAPRMn1lhidK7Brf/PCTAhGmmAhWXmd3d+b+50eh/yYoZGDGXBx0rhmPru7njxBHo5"
                 "2CsBmAnJT5lKghYY57z8wliiRf2TFb/GnimnRIA9nQX/vpDu08futjoPxQHyw8be8eu6hx3HDoEkwmgO4AddyLaxzSIjGU7H9Mr"
                 "c5Io4pkkEh9tu0YbHLNAeZYGjYPzw9qN3Wz8UOojAAovmEg4ns7THrcRV2KIuAY0AMfnV5gG1li6vuS7W5sMhwVJbDHmaRPATZF"
                 "kzEoAlCfxKYuDxq29yuRLJo+ct8LxVoVsmPEjrYz4yd0E4zUAXCN58EyDIAWLc/PcEVa5wHkGk4IwioliwABgIomPgGGWKMP8uH"
                 "as2akv7F9OLlb7Ga+Yt2TbLbZlk5otiYj0XgD9NzFMfMlK1CJtTxh2Ssos0B84JI+wkRARrYAwW1Qjzw7fki2yZ8lRHTcZ+G3Gx"
                 "vFXlEVhACee3DmqUUq1HVioVamvlGC+T2wLDLNEOfb02jfcmDTfJxV3YGI8wvPQAKgggvdCI6qQ1oXVrB6yUGkxY1SgWiYVTjff"
                 "U/na+u8bZz4UKm6dF0wDoCHAH0gT8xu7i5WbwTNrlMDYJtG5uRPpw0sfrH91zx9h5AOShBWejQZAiQ27fOw+vHb6xv/Y2tj93ix"
                 "kcxCYRUqAgJnYNL7QOJZ9c/mD9a/t/S+ShveRsEgEQBOIdAmodoW4/KXlUwffXhnX16y3KQggzDolgGAmUZZMGkelE36Nx8M7w2"
                 "vdv7Kv5JMEI8jLMwBKWPWRu2/p1N53JIPKqgk2BgEC1xslAJjCZPKEvUGeDDdyi+/QKQRjNAA7pUdnar6rv7UlP56dqb0/LeoRl"
                 "C+Lg68MIS63J83+V+qyJBiDBuBlyIphmPUfGmWDb6fF3M28LCixODc3Plm0e39aj9ahYdhBGoDc5kyLstr/Tr+++WBzsPxKG0wM"
                 "wvVNufborLnL3j9/ZN8jFI4dpgEYpT2mhbe+OL988lP1SfPVC521W8Bw/UZACYLxUc2KXTBpDAKgE8COmh8sMy0EITbxGGMdWCB"
                 "w/VIGQzyqNDx5IRseysDVZDQAT7e+cYhp4qLiSH2wcAISrueP/FIGiAjZpOxlF79svmHAcFXNs1sDcLkLS6emLADlg0aSr65dvO"
                 "ENkAEO8Fxf9OCDUDZG28NdG58fhPMPm0rE1TbP02gAhrUu08RH/pF+feNXZLV8S6WY+6nFzq5jkAIOCMwqJUAMWIq53nY+P/hDj"
                 "HxhtNz5T1FIBAzXgAbAhohpIkZIXPb1rfnzX8/y3u8OGps/2dpeeVurv3zcSAoUzBolQAJG6O07/e9Bfmu0sv3fGueW+9ZHBJ3w"
                 "sPwQJUQ+JnGV//39EPz6oN75ubNrD7932Lj0KETMGpUQEE698uu/2d135p1gvmxd1Of5aADU/wuBT785qm//5p8v/fE/LOyohJh"
                 "ZoQxgeXz/X9x/cf3krxLsBmJ4XhoAZcUSYTndOMVW6OPj6E8ebz38Be3lLEkY7Tn3lc7K2Y+IY2C8xbiI56Q7AGWxnK2dpSyFYD"
                 "1gSCRLEqoNEGaBiiizwaBz5NGPNFfkNL6Kky22dm+TnVzHeMvTaABUKZ7GxiqZXQAMP2Aw1cXh8h3gmQXKIkkxNGXYSIcJxkeAI"
                 "CZQrD5JZ2GTpLfENaQBqJ9fZZoIUEpgu7LF5QzGN+18DhEQmGLKCEggGddWoryyWMoAAoDBAGIDUsnJl87BhBdBeE7GYsQgRgPw"
                 "3MQwTQwAIEa4XDB+9Oj8dz92y4X5fxpLnIFnSikxQMywufmNojI6I96A8AwCyBXeP4DB2hSe4SkNIKFE2oeZe2yVcr3EiME3As9"
                 "CAzAzxLo8Lj72jfbX5VDv8PubrrUMgWmjDMFSjLILp8/v+9aHJvS+absR4HmxxAQEIfV1TJIyv3oHoRoIFQF5agByAiEIJjiejw"
                 "YgdcySxFrv6uN/fqbx7eLYmTvvR6brjkEVEZKi3Gyf/tcXFk9+QOqTC3GIwPCiCY4ktLA+Yq3zo7hdkFOCACIgXCbwAmkAwto2s"
                 "6QqhhB5Kv3sohAw2KkKgDK4Vvmk3RM+lY6yC2M/JES8OAIYT2yaLA1fTbVXxyc5gcBLRAMwTobMmmA9Nkl7IIBhmqhAVGHU2tss"
                 "pOvpe4iiiBcjCkJRQmaPgYnxNuclpgHwPjBrggScuJ6LypC4xDJFlICTvOy7USss0jYrSClcKRugvxgot5p4L4AHIg3AS22+s8K"
                 "sESOkZTbxkcsTR5Vpowqcyb3zeDxXSoCsEC7MWZJxSX1or9akpwGolo2ZDEDk4tLF5YjcVJkiyhAyP/Yrk77JX+zoD5cqMZNaRN"
                 "VzNWkAkjxj5hhAKF3stsEuTtMuQBmk4ocyn3cZx1wpAeLg6WcNJkmEEdEAXFXBMIuC9YWPii4Y1DSVGUilJzbk2MCVsgQ6ScbAV"
                 "ohEuNp0CZiVzKIQhSJ435muV38l1mNyO0pOzmFKy5VKy0B3JSVfibB4DcDVVinqzCIxwSUuHYJjeihjIGTlKNTLKw5AFITNdspm"
                 "KyH2gRBztWkAykrOLAo2+MSnEzBMDyWA1MqOXxljcsuVMBIoIouLDLEIO0ADkFeHs7oDKJMi7YNliqhISklDB4QrYU1g21bZsHP"
                 "EEtghGoAizZlFIfKFS8pLTBFlkMyXdpgMq/9jFy+UdUJvCc4es8SFsIM0AOXMBsAVLim6IEzLV4gpARGHM2Oc4QUxELDgAIQdpg"
                 "FwOGaRxwWHG4JnWigDETmZH1IKL4RLEkaLddgQoAdYDcBOam4vzuoSkOq4ngfrsCGekglASRTGoTXpmCLiuRgBX2bkroEJAUG4F"
                 "nQCyPKZDYBz6UCMAIYpodLQD3P+jNm2YHhWZZzgz89j08A1pAHYjjvMIh87QjWcxiBgDFNBGWdrTConnOEisM2z6DSazBO4xjQA"
                 "48mIWSMI1tiVar/xt4xYQJgGKmA3Kwcr/2vpX5brg39knP0sz0Dw2GZgCmgAbJEwa4IJcXOy8LP7n3jVB2wA8Fw9AhhePPmh5zD"
                 "MmCv/OySGbbeQV8uacRGXM74kitsgAQzXnE4ARcGs+b/s3XeUZVd55/3vs/c558bKoburc5DUuZUREkEiJ2N4GYzDa3tscHw9xg"
                 "bb2GDwDOAZgj0eD8ZjPGbA4wBmwIDRgMgSEkI5t7oVOueK4eZzzt7Pa6+zlmqVbld3gbqlbul+aj3rVvequnfVH/u3w9n7HC9OC"
                 "7EvBD4HtE7b+E5OFvd7oQX/w2aMAh4QWGJhqYVHU2iwCMqpyY8QQJ450va66BDbEcGYh6OeU6n0jN90bMWjXw6SiHm8h8Fl9B8x"
                 "gGdRFHyogXdcpwFrsCQ+p/drxL2dADgD6rbO+UbFu6ncxDcn84d29TeXb1owBAYNrLPQZeY6r5bCqIcTPvs+UVAykUBJYKWBlRY"
                 "2hvDCHPxlDW5otocGukDIGLg6D28owAsi6LHw+Rr80ewpelAPACIQAqEBC0RkYmDWL/C5BhDaKWwJ4OV5mPBQ8zCrcMTDCQdVD7"
                 "Enc6r9FAK/UoLf7IJvtOC9M1DV9s/EoNbhh6e/H45UT9hWyBMEjGtSG96AHJWTx5TovLdUC2nRX9m3M/cHUcVcZhIZRHC5cXuou"
                 "Sb9SvVi9wFxVDsB8BSsbazj/KSHmrnKQzTZxEk5eG0Z3t0NBeEJTqGmUAdiB03AAQYoCuQMdAHdBvoNRAKPp3BDAxDmKOQFtoVz"
                 "AdMtsDWE5+dgcwBrA57w2gL8SRUqSjuF3+iCF0fZ5+aAnIARsAIADrgrhvfNwJYI/l0h643vieHWGKYcoADzQ6Ys8GtlGLYQe2g"
                 "BVYWaQs1lYXjcw7TPQuJIClNAoiDAWgOvKcAr89BtIAD+RKCqtDOkherxZNnULcVcgFgDAAIkTardG0DDtpBRlJxaelo5Ko0EC3"
                 "gDuVlzcf/D+f9ePhQ+D2Xu9yqyKZgKNoIMVK5M3maaAtKWy4vRCYBmbuqZn1mKBwAVvCqnJziTVIzKrSMzG94MJxtSGrglhl4Dw"
                 "4aTC1mUiywgzPFZA/9oXxYAlkwoWQjkhDY9BjZYuDc5+UhiewD/rsgprbLwl7NwkYFfL4EDpv1cENwdwwMpzCqMOjji4P4E/mcN"
                 "PtoD2IX//lShBTQVYgUPSBaK9BqesNxCr4UjynwCKDPFE/cdiY/eFBwIQQUENG4QrN6Mzy/DppxUoELkDN4pIkISekZ2Fd7ecyB"
                 "6HijzKSYWKe0M3hIP+m+7bv0MHgDEgxSBsBMAi3Jb7TDPFAWsWoZcP6k6pFRjpJgndcrpeLzT/ImvjnUd/qmhypor26cBAntS+E"
                 "8z8LE+MPzoBi0YAU8GgQmFwym8Js+i5CV7H2LaGXj3LGyP4HkRC7orzkYjm0KoKFm42ay2hPCmItQUPHAghZ+bgkdi+EQtm4r8e"
                 "IEFBQIBUBJOqWSg27QvjiIQKElP/eFm0moGCSCgSUy0ahOuewXiPSCcjDdgmobyMYsJhDQnm8qj4WWcgq1Rzu83P1bd7j5j3FwA"
                 "/DA6IwCnPFMUJVCDSw0pDmbK9LKSfI/De1A97XmA0bhVf5QKV3JSAn9Th7cU4EV5zhyBUYXfnoaPVeF93fD/FMAKCyoKDBoWNO7"
                 "hndPwtUHoMrSZ9vAPNWi5uaF4+2dkVfHw5QbsTQEDFQefbcC1OegxPGWrLNwGKHNQNPLpQH7ZdO/UMKgAEMRw2MC09dhUFwwAnJ"
                 "LrtWgc0TyaIEivevKcRjBjhqPDikkBgWBSSNYr6UrXCYDFEJ5ZAlkJePF0jy3jntkHWdJdZEMwQqopC3HGaZREKbiFF7BihQ9W4"
                 "YY8GNpVPIw7mFSoKjgFgGUWNgQQCtgF1v/qAg8l8LOT0DUIr8qfOgCGDAuTbC5/UwteV6DNzS34chMw2QigbE7+t3yyli1a7ksh"
                 "FTICNzaz6ce1OeZRYMpDABQERMCQ1UKGDVggZT6jscnpjE1CAGwMRzZ5Zobck4f+gXi2omzCk+J5AOFxDE4sGC94z6yoNDkFFYh"
                 "73GhtVYJJBW1AecIi7rwdAXSICs5BbJu0cjUSHOhCAZAm+WapwSlJ1nhuj+H5EfPMenj7FPxtAwIDqQclkxN4VQ7e2wWjHtxCvZ"
                 "eBloddCbwiD6dabugyp45cBW5sDwBS4KYYGimsiuCFEW12JfDWKfhBfPJoP+5gV9oeACj8u0nYn8AKCyM2W9e4NMxe+y0UhXm6D"
                 "RihjdVYy+mMxh4AipAUQMkgYFJZK4l8aNm3iq+3Lcmh4Apab2x0f0tTPxCuCo7XBx2T1ebO3rHwvq6JcBvKSbkS09U17msgNAMP"
                 "1tNFAALI+RsAHdYhJwaoL4G0p44goLRxNm0l9XgWhFOKFb7SaA+AQCAGVCFRQKAssDmEh5Ksx/1aa67hPpWhlJXsfU7nwbR9en3"
                 "YwW1NQOHNBbg8Yp5JBz8/CXfGgKGdAAqPJO3P1xCBRLMRwz4HAP9Un1v7eGkOfq4I18xNHygA0h6IeBKapkZiCBI4slqZ6FfChI"
                 "wwvPym4v/p3p+7DJQMBFUpdd0V/LppyarJl8c/0z0YzTr1jF4Y/9fuabetfDS4GPXMY0Tr6931jYv07+JaSpw4uhqBqGXAxNJra"
                 "+JQKmqZkBTlHGeYp8NaOHKswayvEkc1mlGV1r+9hnPVCCsuDpoznI4nGwFo+7CcdQEZhVDh/V1w+xBcHQFADEw4TqvLgOHUhg2n"
                 "dSyFljLPgRTuSOCyPPxiaf5aQwr83gzcmQCGUzqewoynzbAAcwUGEBj3WRi8dhx+cTJbUwAIBYR2QorVBlYhyEJVKx5f86StlIF"
                 "7c+8rH8xdAko7objbvqa0M/g1o4ZGpU51cvq+B1fuf8dssX4ULHMMY2Ziz712529PH5uiTor10hXNmJ83qXyp757orpEvFu7Jnb"
                 "BfDmb4BYSu8zAAOqwRXAz1liNpCvVWCtaDUVQ8KuCtmwEHCAuTrHerOtqsDyEvsFLg7WX4lTJAFgxm8SslrLC0mfDMs8SAlVPvT"
                 "jykMOaZZ1rhygg+3g+bQ+b5bB3+dwMQTuu4h1mlzaBpv4i+wsIqOxcG/1yDd0xDU7OA8rTRwKe+P65qb4IfjDHWE1UMYd0QNky5"
                 "53D0UuMxnJQiCSa/X14QHQny8f4Z7n7kVr6z7zvfvcPe+z9i42IwgJBEaXXf8NE/vfW+m8cfe/gRojAq9T4Wvn/5d4qf6n40uia"
                 "akp6wIr2Fffbq/q/nPpk7av4Thvz5FgAd1sOBQWYfK6OPLqGyp0T52Ai5sQEGZ5cxOLmcYr274W1y+gZQUTjmaXNpCB/ogb8fhI"
                 "/2QlHmGoVhERS6TfsK/1EH/2UWlDlle/ppQFVh3DHPVRFcP9h+iXB3Au+egURZlFEPFaVNXYGsKJNtSPrbPvhAN4SeTJBNif7jD"
                 "HyrBSntjMZaTGf+tfDllFxN6Nmfo+tQRNfB3JKgYUqgLExQL8W6a3Tv2LSdy9ZfzMbBNeyO9n/we+EP/rghzbqGmrjr/IfyV5b/"
                 "qqu7j0te/AJT2OXeNHJ74bdEpW0/iHjoui347WBKXnc+BkBH4DGBQuAwFtLjZSbHUuI6GBTFtZzxp8/QbAswbbaH8Dtd8KIc8yw"
                 "RMMLpKawPoNcwz6dr2fqBMKcE9BtOSRSqbSOH9vd/OIFfnoJDKSAsSgI4pc1L8/AzJfi1Evy3PviHfnhJHlYF0G2YI/DhCnyvBV"
                 "5oY3xLi+m0FlLIpzQGUqZXxcyujJle1RpPC74Gwqmo9VXbFVXHj04w0Oji2q1XcPXFl/JQz+Pvn2LqeD3fmnh8xfgfT05VubB/L"
                 "eahuL98OHyjSRe+KYw4obDL/sqzIAA6xHqcKsfjCrXhceJSvebBczqqMOtZtJhFUtgczm/YicLf1QHAKxmyn1m5iOPLdU7NK3yy"
                 "Cjc3+KHEQEq7f1+Cv++Hv+yDt5ZgeQAANYUGc0557kAg5xLfE1d8VwLlhOZgzPTymJllMbPL4pnxtc3/e6rpjzfe+dXRTVMzM/U"
                 "9t+6mMjHLtFbZ9uKtvPBFl1AMc7beaDWO3nKQASnyvAsuRSeSPlNnDSgLU8JJc9GzIAA6FCW1CZIGNEdLTLp6zVptcDoK1JU249"
                 "ke+DYnPHjPomyc31PySJrt2Kt7qDCnx8CwPX1QNZTTemMR/mMvXBoBfnGnCBMFpyzaYwnUPSAshoKXyVxLpkNkMkQaIaELyMUBh"
                 "XrI5Ib4v9XW+JsxljahaP1K88+PDxz5h9u+czOjlRNL+uKet/Y92POx+P/WPrSqOfKT5ahUSHwcr9a+NZuHl2+up7VCV6zHw6LW"
                 "OSXBB9TP8wDoaElrCcKvrk5XfnxJfdmHa8fCq44nM6NJGI+CcFqOdt9pwk+Mw/+ogmfOpAcvnJYx2TTCMud7LUgVqpq9TwZ6BJa"
                 "Zp747ywi8IAd/1AN/1w/v6YJ+ARynZAHD4qSahRjK4ijiJQ2O55wdy8F4niXHhf46GCyhC6BoDj8+eORXW0GzApaMAJZZVxk9un"
                 "7mw0fN6Ina8ZmNVwSXfnr5iSV/kz6SvE3uTN/V/a2uT9hG0N9NcdnwoeF/cd+Wb3Tdl/9iUNRrzEq+dbqL/7WVyTfOgwDoEIRYY"
                 "hwOYU4i6csvaW7/4rpk/X+9qHXBr29I1v3e5njjp1bNrPqDehoriyG0O+qyEPi9aXjb5FyDrXhQTsPBRQGsD5jnHxqAhwkHk44n"
                 "WIGRgIyyIM8cp3BHKzvQc3tMm80hvL8HvjCYbXfGc3IKeYFQWBQjWSEsluZ80/fGqfbEuN6YUq5FpJ5UBBXFeKESzz78g/J9H/B"
                 "4IABARTk0PP73D9x3770zdx0Prggv+c21reWvetDsfu9kOPnisR3TL24UmodwJihrqTvoDxrxFvP3xtiLiocLH057/U63Qe4CoZ"
                 "0lXWkPzWx3f9EJgHOUIDhxNKW1sWaq77+8teMzI27p/6ya+usVJZHkhdviLZ9Ym655fpcvFiyGSANG0uGNW2a3/WR3s2clJJyWp"
                 "50RwEBV4VNV+FiFLBg8qHBaL8zBhmD+/P/lOXhHD3ywp33Iv9KCYWEi83feOeCrDfidSfjJCXj5GHyt2d5Yr83Bp/vh/y0uHC4B"
                 "YGj3VzV41wz85wp8sZ6FlgF2hD/UMxc09DXfGye+J+HfqtWXMhxV6fYJigBgsYyGkx+7q/zAf2kFjboXTZuX1D5dfmX4n48cP+Z"
                 "rhyobN/kNb3g8PPCNx3L7//SB6NE7vjV+2/dqcdMLBkV9c7h5u98u7/Zr5K1hGq4eu21syy3J3e9yBapgmWNp2mZyz9pH39bsdo"
                 "92dgKeo5rSClYmI7+2Ld7yjl43MJJTG3lRlifLf3xnbuenV7dWvHTIDawF19ZzhgSgGoJySgLkhIVJVh+vwzIL+xynpoCBF+Xmv"
                 "28g8LtdIIClvcddamHQwqhnQUXmhAJWYFZh1sH+FB5I4BN98IYC86wN4I974OE0Ox6Mad+I1CXtC4p/XYMHWhAaKAMrA/iNMrQU"
                 "IiBmLgREFh7AWFfTYopYBUCBPB7bKoJYbGQwxhAQNKfC6f+yP9izbn3topc310993PTq5JH6KJcHGzf0pIVlD+TG/ue0qTRMaGn"
                 "WYhl3E48tY8lWrLrcCnNH68CUv/uR3bctT4ZvLE7lr364b/cfjdj+/3sBG94CnkzAYz0HPj8ezt7U5Yc4B3UCIJVUhl3/L7+48a"
                 "IP5TRfhARQjAo9Wh66rHnpb0VqQkg5Oc+imAUO4yhzEBjz8M4ZqHMamm3JvTxsz5GSnHo34HILow4Q2s3fMowAfRaQuRpN4cOz2"
                 "QLgKss8y2w2Arknps1y2345salQ9+AEXPZvxhN4+zSEAokACgb4eA8Ygd+fhSlljoCA5nzVGWjUBDEAIFiGogb7b9rL9FgdSRXn"
                 "HNOaVPaov3G9u+B1d9+8r0+xXBytNyvdspfFOCbs1F0exQCRDXSvPfSlTWx8lbNx896JPTfGjZg99QMNAzdfYja/w2JHbs7f9W5"
                 "RBjfU177Ua0ztgsp3q3HjPcZLi3NPJwC8eAbS3i3/2sh/P6elItTbWmZObQgAylNSFFgd0CZHuyqLc20eLgg5KSUjtE8B1lm4l5"
                 "Mrtx8bzv4tzLFwRww7Y1jVfnAIx8mtDNoDYNLDhLbfI7AKoFnh4R3d8EtdsCeFUhYA8wLMoCpEyYwtA1X1c/maA6ZaYxypTxOEF"
                 "jHgUWY1/60KtXTtxNp335/bVd2k61+1rb75lx4Od//zmJm4sax5epvdRBrh1cUqqPPeHzkypd55jEVnqNzsEv+ejfG63zwRTPyB"
                 "c8k/VvOzL6xvbn5QC/a/mQOmwsI6AeCmUqxYBrv6ATAYFH26en9G3JIXLHNDK6HJySlPnWYNb4WlTY+BHNBi8fBZz/vaPBjmKPD"
                 "VOtyawEEHBcl+5scL8z/vwhBo0E5hdfulQlZY6BWYnmt0eGC/o02s8EjKfAqSHXJCmO+Yh4pnQaLw6gL8hzLYufeaT8Er0c6+ny"
                 "hPRmsqF4/+vIntY2QwYYTRAAJQUZRMQ5r7bsrf+faXNa/+2GvrL/qGUWv2BntvezDa/d5Qo4oAVg1WDYo3AKCKERUVikGBGane9"
                 "RCPfvB59R3vPxqOX9cVF1fszO/9xyAnf7GWNRVOrRMAKHj1TMxMYaywqrgcr0ogFkXPdgAUu3z5QsgBTc4aA1wRgdCu20CXgZZn"
                 "cRSswC+U24/WTjj45Rk4mpJReDhtvxPP1hDyAk0FhHmyexC0TxvWB3B3DAgZhTEPsUIkPKEFPOIAaR95bLC0eSCGxAOmPXBD4MV"
                 "5+PM+WBUAwASQKG1UhFZo3WytpzI+U7JxOG9A9cLl6/lqrc5Mq44RA4AgrmYaf3tj/rYbLfbqmHQmlvjmnEaVponpT3uINDpphy"
                 "SBIegroRNVfywY+/NbuffeETd87a7csQcmotmvXair6ixeZwpgEGKXsKdygHJQYnluCSAEJsCr52wQJLAa9IABPCCcFTY7239Sm"
                 "4Os0Y23AFlcmLylCO/sok0OKMj8xuRoP967LcymDg8mtLkmAqF9ce+6CO6O2/f2x0DEnCMpPJoyn89OEm4MafODGLoFlIwVsGSh"
                 "+JZCtk263/KEqoNUaSeoOJrlqR+kQeM+rwnzWEt3PqISN2nHgazmGAyC8GQqqIp6BNQA1oDigO9m9ZR01gACLPW0waPpXrrDLnq"
                 "ibkITEBCc8RGBE+e9uMZZbfwobIyyhbFMe+O6LILbWpyeZseEP9QNXUKbLgsXBtk8Gcmq4aHlIW94wqYwC4EH4yfPo9vPJACEkt"
                 "0w9DMNOOLmAkaYz2dnBGD+2QisgatzMGBo8xNFeEkOhEzZZLUtbF+LyAIGYqGdQODJFczUgO9C1DIHNIXXbdjMP+68l5lmEyPCQ"
                 "hyOsitS0BwOz0kpSGCxvXl0rMUZ1FkEFISAkGpSYyyZYDgapLfQhRfmujOvPFWpuGZLWgchBQzgOfMUfrsEecOCfroAX67D4VMF"
                 "kcKwgfd0w8qABf1GCW5pQUUBgexlvoAskP65MTcNwMNVuSwcTuZ5Ofj/yvC+aUj15AHgyOb/KHM8rA/hpTlO6hV5fih7FZrKyfj"
                 "A1+NifZ9PDKK0iRNHmiqnoiihBqAGj/JkiiqoJwMCEhlodQLgrARBjojJeIqGaUKoGLV4PDZrUOCEBYniUQRAaJPiUou5pyn1JK"
                 "/lEJqAcOYo7MjBTxQ4hax3fEcXvL8C08qCtoTwqjyn9JoC/F4XfKSShUDZQCQnb3gXh3BbDCjkBN7VBXlhQT9byo7ifqcJAF5BF"
                 "nHg6bpc9llnQlXB0Q6hHk4fPlzY+52wledkrDP0dHsaU6cOgKIWUOX0I05VJGcxXQatK0gnAM4Kg8E2La1mizwhKZ7AG5xxUHag"
                 "tFEgwFJyeVoaI2rweAIsIAAEKFVbv293bs93Lm5e+cozHuOBwAe7oGQ4rbeV4PMNuDVeOITGPXy/CVsi6DUs6A+74StNuLMJl4U"
                 "gQpsRmz3c464YIBtZvL7AKa2wWUg8mMBYApMeEp0LTZuFVMYDCqvD7ISfCGfEepOFVE2ZY1CjyYnufV8/wJ7dgc1xcsqS5QHjsw"
                 "GJAzlFCOjCAaGKKhnUg7MezQu2LhB0AuCsEQQAAbSuxJKgQ+kCAaBYXyCXhKxojDBlZyi7IifMOKKCF4/JtvmO78zv/MhIunTHc"
                 "LpiKdTO3KW/ooErwvk9ZEVh1MMxB4dcNqc+7KDqYb9nYQIPpvBTU3BllDXgZQa6DRQEFGh6iIHDLquSyXrthfxCEb7UgJLAe7sB"
                 "YNTBpELVw4yHKYVYQcjqoIO8AQw84uZnphV4cxFSsn0C326QNVYPO7PAoKXQAHKABSKBnGQ/F5G9FrMiEggAJZMAAwZyQI15fC6"
                 "tFVfkb71AL0aMYSEW4Z50F0YsIG0NHwVROWXvr6BkQMHnYHqwweCJmNDZTgA8XcQIqHCKuCYlZWU6QhKkLPdLiE3KdDBD2RcJfU"
                 "iiCRVT/87txTt+44qG/5Olyco10AA8T41AU+EXp7PGqkBDs0Y17rIQOOqh5dvPui8sC41DdeYxAkpWMPfNL5ezAFpIv4U/64N/q"
                 "GbP2zvm4UAK0x5qChUPMwoJGQFiwAEY2BnDsRSWRDyh12SPAnubwg9KcEMzu5VXTSEBYqCpkBMwQEj2fQ4IszCgkBWRQCigZOIs"
                 "JKko8yli1fV1DcVD8fLTdiIvXh3y/UO72nI+JEROM/RXUfWiyhzwQiOK2bdklMKEIUgNobHkbUSgFmMNUT7qBMAzJZEUjyclpYs"
                 "SM2aGos9T0AIOT2o8+3KHvjARTB66sn7F+y9srXtlcCae+x9nB2lAyOgCT8kVFk/a388zHwJbQ3h/N6d1eQjjeXjzBFT9Ip7aKz"
                 "yhpdkpwY9HtAklu6JwVZSt6H9kFu6LT/H36lM7uybqXZi2PJ7T2bZiDd/Z9wA5G5IBrx6jlojwtL2/CMp8BM5Sixo0B4QwseydO"
                 "cFxqVAJq8Sjnt0/eIj1rOsEwDPN47NXFIfHYEBgKpim25cLVlmmOMCchYOW8vQ8VsUo/HkPLLHgFB5I4eEYHnMw4SHOpicUBYJs"
                 "VIETwPLDMfDpOqy08JtlKBraRAI/VYQeAz87AZMKCO2Ep0h94GPxnFaTFq/afDHffOQBPIqoICoonkVQTkbAegMhxJFnvDGL12m"
                 "MNZgqVGeqnRHAuUSz+f+SVNzQYNL/6EDaE/emvT+7Id6y3WgTUM5fAl9tZSv2t8RZA5/9t1JImWOywgEq/EjqCh+owJdbcHUIaw"
                 "LoEXjcwe4UjjkYtjDuoQognHmKeHxwtOjEybwNk4GCeG17jMBW1vJIMko27BcWR1BQj3oWolmJCFYsAGrAGNsJgHOFojbU8E0vq"
                 "Dz/w5EGYc00Rh/L77k+73NLrDrAAJ7zlid7ZqAqJKfoZX1WT41AnWwj050tyAOBgYZCrMwnnC0K4HE4AMiJ8Gic8HAxZHo4ohUq"
                 "whyTOtbsjHChRVGeIzoBoCiB2q4d9a1/NJAuWQMJXa57eV/at8VL4p3EatUI57sYQHj6CDigpoCSEZ42oupzaSrWEFg4MWM5UId"
                 "KtzJWgEYERpkjAbWXbWHTt3eigWGxVFAB3wmA84sRZJ0gqwWp5shVetKuJXNnVyGnQYQGgGbVcX497lVQn9c08Mr4OBw7AfSABa"
                 "xmZZQnKBAXIlSEZ6lOACiKVbPEo//puulrfirvcyWH15lg9mhOoyJ45ijnqw5BBW8LPjl4osmeo46VwQDCwkSVpBCy62Vb2HbD/"
                 "SS5kMVQvDrx2gmAc6zDUdW2xu/Fly6vXPq/tta2vwY84AChGJdXgSerZ4MOG+An0lbt9qMVlgblsgqRF60rNDkFbw1xIcI4v+jR"
                 "gKKcCzoBoCAtQQWiMAAFVRCgZhtcPrPpnRfVN78CHFkB6LOw4Xck+HSqkUR9Lv+y7iT30wWxG3pa4fenVP7KCwdoh3il3lPkkRd"
                 "vZtsN9y12FODprAGcCxTxgj0akVpHT38PThwmEjxKyZdWXlS/4A2hRgG0eHbrcA3T07Wr/89fPt53XYEc4GFKXxjlmxsOrYjf5o"
                 "UZ4WQUSR0/pM4U4FzinWdibJqknJDvj2j4JltmLnzFYLLkInCA8mzWoeQb0cC6xvB1oEBCRth8KHrTw6vcP+xf4r4UprTxCoEHZ"
                 "XFU1CvaGQGcawwGk1iYFExkGE6HNhVdrgiO54IOBRzzKYUYWTJtLp8t+utzqaQoeAOiYBTUGnJVEHUgIeiiQoBzTCcAFJCW4EY9"
                 "JrT57qDrAjBAynNZh1CIZTBKTM56UgRKdfACtZxHvadZzDG1fIju0Rm8NZyKourFcw7qBIDHRyHRhjCxl9rUbkBMZ/TfwUxRH+u"
                 "pU6sWlEYE5ZoQB8pMPgXAdUWka5cycGSUVlAEVU5OJXSBXjizqrMGcC7x+HxEuDVHcVuAXeWNL3kUlOe0DmG8xx1LAo2HZsxPtk"
                 "L/nUakoyoAYFQAkMTRKucZW72M3iMT+MCykEAD1lWWcQ7oBIDHFwPs9jLFHQHBSostenzS9PHktJ0Z9ZpsNhjA8dzToaK0AjXPe"
                 "zT6jVJThvcPN19faDEq2n45sFUuUBnuZejAMVphAXThh8nENu0EwDNJ0TJwSZHCdosZMZgckHp8TQBB9CjHD1SlVu3WnvJzMwA6"
                 "RGHJtB0OnCyp5n2aT+hqhjqYBowzHzZOqQ73cGL9Cgb2n8CFAQvxnY1AzwxFuxS9vEBuh8EMCRIAXtEGGRTIERaOudE9B+3BfVt"
                 "l+zbUAJ7nno7AIaBYj7v2odx/d6JJI9LdP9gY/2fgTjKIKnExR7O7hHhlIYrSWQR8minao+jzihS3W8wAYACnaEw7DCYAie/Qe7"
                 "7db3qHR9zqJRA/h0OgoxBLVJiU9QAqsjGXsOmz16QvFuUEGVQV1J8ru4A6AeDxQzmi5+eItgmmC1DAAymnpjmiQsXXxr9uvvvZF"
                 "9qrX7/erV8rncuCnWOKgKgyMhls2Hg0fJ0onyQDNsBMW1LLqe8J2DkMdFZZ0OGQ4PkF8tsMpqRoCqSAskiKEhHla74x8Q357j+u"
                 "t/su3sHm5y91Q/10dNIAdOmUWSPMMcZSbQgVUUxnBPC0iwSWhYRXRURbLZL3aKxoi6cgwOaamtSnmT6R4lOQztbgDrxBDw2kO0W"
                 "FJwSCTT3RhKCdjUBPG2uQtQH2qhLFzYLkgKZHmzx1EpM2u0xx6JX6kjf3+sGuzsGgDi/i9g7Ftz++NLleVMmAixxLqikrUyUJOs"
                 "eBnxaCrOim65cECUEbitYAOUPvTYJrDdG/Mq+lCBKe2zqcUd0/lNx575rmz5eaUh0rpYgCgDNQLRniYm7B+wNkI4BOAJwxIcGII"
                 "KGiVUCyOnMMYmLSpgUB+xy/5VdHM1St5f34+uPhG3qr7vMnLkoOWg8ANnUc2TBErpGw/r4jxPmAJ1PQzj6AMyjAFs/Ww/kVJSTI"
                 "jenE4aNy9Nhq1q5GQVEE4bmno9QyZvuB/OuA1922vv6SMOWN1kuiKFEKOVXy9RTwtBNUVFVUOwFwftAAE8WaVm+S2756gZzYOmj"
                 "7V69NV60MCASU56IOBYTth6OX3L2mMRKlcsB4BVVCVZrdJWb7ihRrCd4IT6Z0FgHPGA8tziIFjQjz037m8M3m9r0v50U/ZyVaiX"
                 "qe2zpqkU62Aj/TWw/Ix4axroSg6Ti+up9oZpaeqTFa+ZA5oNBZAziTEpIK5JWzSFENCQt4bJF8XtQIOJ67OlKryf0rm/9UybnpQ"
                 "p4uL0ElsUoRIddIGB/ppXuiTrHSnHePABVPZyPQGZSSjioaAwKc7SBwD8iuO9bI2nU5DS14nps6Yquuv2ovevOdPf9iVXKJ1enH"
                 "h+ULx7vjz9lUmRjpYWTvOF2TtXkBAPjOIuAZpRMJ6dGIcI2iDUDO1iggEJvfyIbtAfY5Pv/vyKWS23Go8FqrQgZWTUQvveWCypq"
                 "7Vzc+kq/HHLlwCbl6Qmm2ibNzU4DOLcHOIItNYuJ7c0QbFBXODklIG+vN6iu2uM1bDTzHA6DDeuTJg87uZjhwxf7yOw/3pbcf7k"
                 "9umhksERdDyjONJ50FUM6czhRAHe7hAvlRi+1VtAUIZ5jH+WEGlguBQEJHByjzeQYrwfD6E8Grxgqtm8KWI0jauiVVVDkNcYooa"
                 "CcATi0iwuFmGzTv7qL8miwAzjyDkWlmxhT1AobMvCcBd3QIhqGxdP1KrXZFGlVyTYcaAXTRdwU2Lc/MxX20BvNIqpxaZyuwWOya"
                 "HNE2j28CwpmnIWFunz/0wEGzf9tqv26l4HE4TaWhkUYiiNDRgdCKm3GlMp1GROTSlJA5ip5yDUASR7x+kGRpCWc8EnIanQC4tET"
                 "pTQaJFG2erasBgthUXfObfO+f1pr920sUSqNMnBiQ3iUvcNdcAymgPJd1GFokxH3T9wwsnW4FhAR7DcQCMm8KwEkpCCCBBRFQBZ"
                 "VOAJyKw82kpHcF2PWC9AkiiurZeIifwQSJJvWduvvGmDQRhEFz6euQADTlua7DIwhXdA++/Jpl9itI9NidR0Y5NttE5i8CKk+mk"
                 "Aaeoa7lxPluprQGwiJ0RgCPe/zjVZpFi90UEW2xmFWCFAWJAK+oP1NhIIgUJN/dJ1GuaPJdK2VkDUnn8WEdAkBECNX8IPVQkRzG"
                 "W0A5GVWdN/RvreuhlevGtnznKsAPS5C6IHd7/N1NmksD7JaA8EKLWSJIQRABnKJPqbU6XLo6XHbhtfKC1+fTfN6koUDMc1mHQOg"
                 "95Xgv3niGGjfQ5fZXmrPMSAMvikEVwIOPg1QtljC0KIp1FkwOH1rEec5HhnOIwRxPcN+uUP1EncZnY9IfpKRHPd4J5AT5t7I/6g"
                 "igro1K5MOccWUBAMtzVYdAMamw/djHWjuOXDe28fB1R7tn/uhEI0y/++hh7ksPUYgiEGkqeGd8OtlVVS1C3+oi3avzDA8M/mttQ"
                 "oe70E4AnBkCCOINZndM/KUa9U/922tCem+KmwA1c9OExS8cGoydcNOjt8htN9wf3HnnVDg+iTWA4Tmqo7s5Tl/jpvExU/xuZXzm"
                 "X47NyncnYmZjQ4Cj3/ZdtIrl1wZoVErzS4brfdfFkua8U9Qp3nu8T8Er5yvDOUyyrxlB7moR/2OL1mfqNG9ISHY5XCMLAikLEiz"
                 "ijh/ivLp74odv+ra/+Ys3yLc/973gpq9NBhPjEPJs1yHMpzBaWs3tq/6ua7r7C1snRj51xdSyv+hLguvSvpChcMmO/rjvb7a3Nr"
                 "09UImGGr1rrz667Z9H6gPvSjQV9R6jSptOAJzVMDjYIr6xRfyZFvHnmrS+k+IOKmoMpluQAiALhYEgUqTQHflc7lgyvm+UscOIe"
                 "p7FOgIgDxjaeDFU8qXuI8NbN59Y8+bLjq/91Uv2jvyvXLlnx0Bx2aWrm8uvMt4ACkBXq9y7rbbuF7pLvVG+1Es9yiMoAKKQBkor"
                 "7/FGOwFwloOgBjzcpHV9QvqZmPhzDZq3Ody0ICWDdAPRyYLA4V1kgujF0fNe/2r32p/qT5YNA4Dh2abDMM1sa8/Shz5b33D4C1h"
                 "NaOOAFEiAlOHZvjXbDiz7j3Hc6q6b5hh4Mgqk+MCdKOVNaoKARljCaNbgG0V34ZLj0Z9uv7frE1FsL2rlPEmo/1adqwBnOQxOeN"
                 "yJmPQhh1uiyOocwUUWu9ZiexRNFG0CHhBFfShB7iIuvLiUjpRSOZa2bNwquUIJFUB5tuiwzIQT4ydaJ+KhxkUbcfkQWoACQjsFE"
                 "i44MfhqU2outyJFUOYIs/VK/MCRA45VK+gN3KuaOVkSxWbPygPF31m7t/zjQSqIip/uSX7Peql0LgM+TQzS8viDCe6gxdwfEw8Z"
                 "zIUBweaAcJmABVqCuFRd/LjufWhlLl0/aU6M3SMP3rTSj6y/Ir7i2tBHITieDTocS93ywcG+3CXWuhNT7ujuvurQRsjN9fptHLn"
                 "U5C6orLgiUFFQ5iiiub7J7i76GrlX77i/62+Mo7T6YH6qdyq3yjoAYemx3NbeqaAoSicAnqFRwWyKnxX8AYO5vU59ZUi4JcBeaD"
                 "Hdzjt3a3LX15dHB9ZcY654zVXu8leqx1sVC8r5rkNAgJ54KlfJ9+WOLb3Abzty5xQTjzf2FdYdM3v25rTYtTxZvhxSTib0FlBhP"
                 "vI+6h2oFK9d91j4iz3T+RFIoRL0gJIVTPUkJ6pdSWK8ALCiEwDP2OXEVJBJh5s0mEfqNHpDwgsjwq2oLp1Kq/W7zYO3rJeVF21I"
                 "N29CLRBzvuiQucIDSsaQdjem6uun/zRI7EXFw92vM/uW/dxwfah1Z3DvrQ+7Pfdtkc3XLGfF8oWvJCvtlK56ftm196/8pzCx3e3"
                 "nSATwHB2ufmPfqsaUeAC4uBMA54Smxx/3+NGU9K6Y1tK6a25IW+kLt7HjGifenwgOjfa74d68RnlwnMs6DKlxSXX17DfKobPBY/"
                 "2vQg0+iJ2oiq0GPYUH+96pOUkPjzz25/cnu/9ldKr5uj4Gtr/Jv/6tBY1ySoLwwzGK7Wrmh08eEkIcJAQN1qfGd7lQZ9HOVYBzj"
                 "Qfqiu5N8d/q6o3+tn9r8zN39t7615/Tr33i7uD++xNJPRjOTR3OeDcxNHvL2Ev3vyW8euotQaS/ztaJ60EAtXF//YjvTkfDONcX"
                 "NsKh3J6hX6jttz+Z09zgDjZf1eN7uyINI+FHpVm18USp5fn3Lfntyx7o/5ktu3uCrbt7OmsA5ypFvcM93tDmb8W9+W3XJC/+H2u"
                 "rA9sh9WAM56AOg1s2szu64vivDxwvHyGK38V0/o2MFdZSbtZFNdQefVSXTx2v77EvbNTTsHd2YPmb/Y//LqKIcpbPgAjWE6Zpq3"
                 "WHeTRNSHkBOzoBcC7xeGJSmsTcN/k4+2loefWyB18y0394UJdejbYA5VzU4YmO92yKbsrfyKrZG9hTLHO4Zys4aBkEyD0evpQD+"
                 "TQSnxTiXF4QAeXpucwrJEGKVJJro5K5CQ33AtoJgHOAIKSkVKkhGCwGIcJPThfrk9P5hwrpDavCpa/sjss9EHOO6nAYpgr9TBV/"
                 "GhRIyRjAIxhITBBA8PQ/E9ITpoYrDq//WRObsuuv/SQQdwLgGaZ4HCkeR55w3v9bscORyV97oLm/e6d56IHLueyqEBOC51zV4Zk"
                 "jePHemySx3oSiGJ5xjr5Kcd3Iy8aKnQB4Bhu94vCk5Eq9CHk8njkgIjRNvD+f6x+/YHbwDVPJdHXKTlSG3VA/54kOoWVbjUpxcq"
                 "K/MbwkSKLcMx/eSldf6pko/iLwXzsB8LT39gnFYh/5oIAhpnvpCoyxPJkYQ3NqinpavWdVfk2wKV7xaodPVVJEhfNBhxL4ICw0y"
                 "93GGQvKM08ZisuXMNO6m6dPJwAcCbbYQ7nQRbl3iCDKUQR8muCd48lUoeQLXfHU5PDdwZ3fKwfhjtXpiuWiAMr5oEMJfRiFcX90"
                 "dm7yqoCwMJn7GZSMwqrpT+mK2XdKJwDOHpn7wuPoKw6xbGg9Qb6AS2O0pWQinkyARN3wMtfzB89Lt7xWXVKITJTzJAqhcB7pUCD"
                 "lzBIgR8YxFy4mKwD8vAVIREEFMLB65v8IzHL2dE4DOhwNGiiKxxO4FicmDuB8iiwi1+PA1ZZxsVljLroA78DVeTbcKrxDAG3vvb"
                 "FAAPisEDIKODICBKS0OMqh/Q7ScsGOD2j3JtMMe8gldR1s7KKcVMjF+xCmpBpdTuDLHOzZQKPcTU+lRjmdophwFnQCQBA8nipVU"
                 "lIEAWC6Nc5ka5TFUBSLLd0X3PNgl0QPXCw7tqMh4LM6D3VYUokVVQkoAgZwgACCp8l46ei9vcOmFk32XsnyyteBmNHSZUzkVqHW"
                 "UG5NsWbqa2ZJdc+x8V3Xt1yabAo3vEj2FX+XNCxxyYm/Z8XsnzBeTOhqjuOlodXorTJdfBfdcVn7JvfJxSf+goHGfRjtBMCZz3W"
                 "lTgOffREQoCgZg2VxFCUilCRt6Q+448ZJMzmzVTZfOqzDpbmDQY7zQYeA8Z4gMcYZ8VHCXnnkhrTJ4LAObI5NXJkMpr43Hox9cS"
                 "QcvKO8zvtoS2U1o8Vd9Le6Wdr4eR7o/3nGu1cQOs8Vxz5mepMHtt6y6aN+PLeuNN2zXirhECqG2dw6BlqPUYsgUggcUvDfVOwmK"
                 "bcqNO2X6KvvBFp46QTAWfBEr28wAAjCj0KQMZAvVKjeda9/8MI9sm/jkAxtWC4jW7awYVvRFyJQznUdAv2tw3rF0Y9KNRoNlkmr"
                 "/uDY7Y1dhaBp690lKSTTZnpiIpicXKFLEA8sr+5jaRMatp87l76MmeIQpDBb6OPG5X/CYP220qODP81soRd1gAIejnRdKvt73qV"
                 "9zc8R+H0Erh9vjlNM3ocjpWkbpIazrDMFOEO8otMGM+NwDx/V49EstVcuMUMbrLeGc4IAAeAAz5N1mKxWT9/M+qlPyGP9CX1gI8"
                 "FiSUiA7HurFgRwZHpaUC1dyEy0Fa8RAE4M+3qvYX/fVahaSJhjoGm7uW3kfWL0l+ltthhsPMBA43dphIeIkvPxpqAdHq8paV+f9"
                 "P3S680r//QKf9WVOS0GYIEgK8JnIDMNLRu3DgcHjlSl1gDL+UF42uSTOheOfZu1M5+nO0kopJAY0JN1FoIESn5zDGKgHkJX8nVe"
                 "te9qLjnxJaxCT3MG6+DC8VtZN30vxniwICjdrRo9saOUKKlZTin+vg40/pjB5lFZXoF8Cl46TwY6f84GOBxNABQdb2nrmzf72zk"
                 "oR65cJsOrixR7rZjQq5YSjZMCUTiiK0YEBTxnl6EWzlZuDL5//SPxvvu32ouueoV/yRvwFnCcqxS8I3VCYCxYUM4OgXI6wyXHf1"
                 "+b8vd4beHNafNHAhALpAIoeCLdOfBW2TXwY/S2GpTiKdbM7qZph9g29tf0NW5mqrCOofptbBy7nsPdryCf7qWveS8tc5CpYopRE"
                 "LKC8zQAOryiOx1upyDcIndSCroiJy460Tr2ypBge0kL3dfKVa9doxeuDQkCcIBydnjyLl+6iitefkG4dlvZdXXjBfCcsyRgsnj8"
                 "wC3m9m8vaYxsvsxtvyrUyJy1wEpMQC14BVGymanc5/jB8C2aCjKYEliLMYIng4IJYNXlAewr84TAD4hIF8P1b7Gy8kmGGzcx0DT"
                 "s776KvD6E0T2IglGwCqL3M/c957OABXVIVjEQN7TxBSjur9O48mt64+xFcvDKy9jxvD4d6rWI/GiXDg0ZD6KgZv51aRTrAzPghw"
                 "cHkqWDoEDCuc3RbYvd28MLL2zGvhD7uBVqVHgqD/BYmIJNvY7nh+hnP72N4zgDEeh+uGBFLwcOesYmEgg4lX3AL7Z/LF/mWS5g0"
                 "ToUf3eT9EGD3XGf7np0H4fuv1g2v2SjbtrSQ09RsItcqDOAxZPigcAIGMAFNGkkwbL6ziAO+hgvrwYPpJw3VAlnuwbWsv1FAJAA"
                 "jsVSUa8qRhBEFJQFGIh8rM8//Bd0xe9m10B7jqiiSseZWwTsECRW/J0p6WenqXzqRm7/wBflX/7yPrnn/mmmG2CBCLALrOSHqPH"
                 "M2BOP3mFu+9LN8r0v79TdD+xND+x6SHfevUt2fiR56b7ruGrsT7GqnJcc0FBK1Vm6mxMEGj85/LJXwxwDxpCumrxxdvmBP2usPv"
                 "zXum30cxR9DYSsTFYIBB4KcVOWNz6LAXrjp2/xrRMAHYK4APuIKF85qMc/8lVu/A9fkq985A654/YxRmdVPJAHck8EQmIajancw"
                 "Tsmio98aHfx9jd929z8xm/qbT/3Fb75ps9y/Rs/yRdekV+T/mHBlRVVCFIF4fwTQskpW0/8hV518DdYN3kXIoCBUlJjZOabrJz9"
                 "GuV4GgwYbbJs9i4G6kdtj44Faxqf8RdO/Tkrq7cTuSoIWA/lJCbysGp2D1cc+yuW1L5G0e2XoQS5aBoSw9OqMwXoEISIcAxlbC+"
                 "Hbz0hE599UHZds0aWv2i5jmzot70DhUDiupna1QhmvjkTnrihIIXD+WYXBfIoOutUZi9dvgLpEjZc0Ave7+AHy99HKzCgnD8Etd"
                 "65gendwfrKDxiuf5qhxmM0opfz6NKrCVtw7cH3E7qv4k0vDw38d6rFSyjETVZX7uZAd9E8NPSW8sriVaTiGc2vJTEQOLh47G9om"
                 "nsppX0MtO5k5ew32NsVkUoMAokB4RnVCYBOELgypd3HdGz3AY7876UyuOLicPWSJcWwOWPHHwx9zkWuhDUGUARhhgbPG1nNy1+4"
                 "kaA7t4K7ipdob32tCH4xR1IXT8goZ4/Q9Mnk+Mp9f7hya/A10lSlvwVdyQFGpu9n+exXWTfzt3xr9Z8xXtwEOsSOo9czWnw5dyz"
                 "7FbwFFJpapBb0koQAsGJ6J5eOvYfvLx1lzSxMF6BlITUx55pOAHSEBATYpEhhX6i5fdYHBJLDaDCvATZ9wqVrl/FjV28myCkaVw"
                 "aF/Nvl7pFtpCYEJRMBFoiBFBAWR5hjAAEUcCxOyNyVB1nUbsVKUDm+6/jYN+zj/a2R9SEo0NP637pu4kuytP4A1dzV7O35KQqaI"
                 "qnlymOv4fG+g4R6FcsrX2Uq9yLAsqx+F8fj13K8dwMDzb3MhCk9MXgBz/mvswbQEfuU7WuWkusLUW1B6B6hGfwhVivU8n1gcOL9"
                 "kcL+I4/ndj5csdMzc7sRzWkbIwhgIJ/EeunRv/nX+jOWVB9FOA2LYmkEs87bxEMJCBZ48roBAiCgGs5OHOg++KHZZlw/dqwOVgD"
                 "Ay35i+wA5oOT38eLDb2P11Ku54vg7Se0+BhrvZc3Mz7B58r2snf33LKv9Eiurv8cFM+9jy/G/Yk314xRclY1TEHqeFToB0CEIrS"
                 "SF1AMCzjR008Rtet2+3yHXAlFEA2Nbtq+ljXxs0hZYWjRxeMDSztDEc7B3dOfo5kO/z+Un3s+rDvyW7Bj7sKyb+TBbx/6SrmQWg"
                 "gV+30LeU10xuuvG4HtfuJ5vfOVx++hBZ1KQPFAGSkAOyKMo1aAydbB44NOPlR97Q802PhOIJXjy8oUCkULeHWNV5ZMI32JF7c9Q"
                 "KjgzSWJ207KQmH2kZhexibH6eZZV30lf8+t0xzGlFER5dupMAToU6G8AXM/L9r+RZjhsxgqvG54ore53xZwd7x2uDB+77bvp9z+"
                 "6Kr/ksosbl72LqZyd+2VQ66msP/7ZmSn3XtdX28OACxhqeFp2KYe73sXe3tdSyxcZrh6mt7Gf/T2XEpsiAIKyduJOtsx+0O0Kdh"
                 "/VseSwG7/okBzbOCADFwxJ/4qSlLojIrViZqrU9tqcfSTOx3f2p73767YxbdWyIM2KxMy9Ws+ClITUJDgBL6DCs1snADqcAKQMN"
                 "L9EKxWcfMFUC/mop9XNCx5fl8zWHhm/Y+rxPlv8GpePfpequZJ6cCnNcISodSc9zfu17r5oJ6IpkxrwJBiFyfyr2NX328QBBClU"
                 "gwE018QRkIFAY7aMf5Ze/xWJe7BYFD1S0dr3YlyQShr10mXzkieQMJ1iupk3hboGjqGkH6MGL44zoaMTAJ0gcKI4mcAD1h2ht7F"
                 "LWg7rA4yzDfLptzB8D6N5RALycYNy3KIaeDIgAALF9Ha2T3yUpfXvUg+q3DP8MY6Xd8x/Wo4XjJlkNoLls+gRQZDEYJIAS4Cd+8"
                 "I88epVOZs6OgHQobQPg1XAE+MlRoXs30IbBYzuJO/eQyFNaFi44sQrcaOv5kDXjzFWvIzIzbB69kusnf08Xui+wHJF9wCPfv0oh"
                 "f+/PTsoAAAAgRh02r+z9lAIsc9yFTUP6g24AIAAAAIACAAIACAAgAAAAgAIACAAgAAAAgAIACAAgAAAAgAIACAAgAAAAgAIACAA"
                 "gAAAAgAIACAAgAAAAgAIACAAgAAAAgAIACAAgAAAAgAIACAAgAAAAgAsHGAm891kKiMAAAAASUVORK5CYII=")

FAKE_DECORE = str("iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAABJeElEQVR4XuzUQREAEBQFwMeIILpcKn0lXIzdENuqKn8Ceu"
                  "4BBAAIABAAIABAAIAAAAEAAgAEAAgAEAAgAEAAgAAAAQACAAQACAAQACAAQACAAAABAAIABACMPGTPlZ8d9u4Dyo7jvPP2"
                  "763q7ptn7uTBIJMgAQLMSQxiVqAkK1hWsC1bluS15LDyamV5HTY5yGEt73679tqWbMuyLVuOkmzFQMVAMUjMOSHHweSbu7"
                  "vq/bR7zxKYMwgDECCBQT/3vBwccIg7xDnv/1ZVV1cLQq8OYCxEaYUkaNCKZrAaoMYjYgDhAMW6iEJSJV8IMBYURXPJhpJf"
                  "8QPWFW+W2eACaQdFvAihOi0n41pJvq3l9Ks60voXmch3tD8GK2CULhBvkXaATIdo2cFIgjxdhNigKztQ9EjTQkcgUkAgUC"
                  "h6aFgQoOKRvSFackhioKhggDkDfR7KCkqXAIkg0wFYIFTYZWHEQ6SQADmFioIynweNFcYtxEC/g2kLHrTiwCgya9DQQzVF"
                  "cwoK9m8vygJgiciIotatys0M/8dwT98PB+1CD1hA6VJAkNloENhI6N/ph9oP+WWt3yTQf0KF01AmC4CMikdc7hWlyVUfCu"
                  "v9KwHAd2se5VmJYHaXLjATuX90Xj7gVzd/CS/KkpIxLHlZ8xtv31jed9YnwvrgygONvxgeYou9v+8Xzb78L2CV00ImC4CM"
                  "0G3+8Mb+mXP+KkhKeUg5dgoqmEd6/guxWYcXQECEU0QmmwJkFAVxgBz0yR/0Ds2u/5Mo7S1AyvFTZC6q2J3Ff+fXNt6NM5"
                  "yCMlkAZMP9LvAmpdwc+blyc9kGSDkRZHvxLbqm9TvSCHbT5yBRTgGZbAqQsT6g0hjD+gjjIwKX76vWV/8bMJwYikyHfczI"
                  "a4jlJtlS+F3Zlf8thOsxvLAy2QggIwQuDyo4G5NLKpcW2v1rwXEimQd7fsu2o35aIaBQTH/Zb2z8so7GH+D5l8kCIBv2Kx"
                  "5QUECFXFyh2Ol/udGIEx0AdrrYDwAeAJqBMU+Uftut6fw9RncgCsJ80i0ChUgNsVYRlEinsYDhWGSyAMioOFT8sjAtrgk0"
                  "7Afdr+J3pibeHaVFcnHP2eA58ZT5FGo2YDz6Cdq2j1hKeP4HwpMAWAUYpi2vlO35m6mZtSRmBPDkdTcV9xSj/pOE+jUMHQ"
                  "4vkwVARlFUdFU+rv5yX2Ptm/Jxz4DRAG8SOmFjNkyL36iVd/2Vt3EeDOA46QTsXZXfpGMAgbq90V0/dyVWQ9kX/QK7cm+X"
                  "8WAUBRAOsh70Jnks/05WJHfqeZ3fouQ/w0KZLAAyioLoxcOzG/+x1Bk5BwTwgGJ8RKGT7y10Bl/T21z5Gi9pDJ7nhQIdQ5"
                  "fC3nC9bM3/keyILpFd0SYQQOlSFogFNueukn3hp3Vj+w8YTv8D0KErkwVABhSQkaH6+u83/9g5kDCfAg4A6yIsUQTKC8IL"
                  "5q7yj6ECaLeOSqEhyHcLP68Xtoe4IH77vBDIZAHgtMNSIBhACCkgLIbgJGGwvfY3ezorus1/RMoLTo//55AHCz+iA/4Jzo"
                  "l/nUTIZAEAgKIsBYon0BxGDZ2whagcdaXfanj2UHvtj4NyJpB78r+kK9J/Iq+P4gEBccKSkAVARhBEDaHL4SVFMIeNPA8U"
                  "0p6r8q43D46lT2HOFtgS/jgrk18hEcgpqAFhKch2AmYURCnH/eAVVEE5qBTrQ0Kf/3+1BgxnEtkbvAIn4AXZH4Cw9GQjgI"
                  "wXh5cEg8ybJkS+SECOhp0iNq0t4Dmj1M0APVqkQZNJA5ICwpKTjQAygsCCAusDQKmH++9sBFMzYDljOIwIibQsABjWYrgG"
                  "w1UYlmEBy9KTjQAyKh6PW1FIq/9psH3WjanpdFS8B+WMUfR1ZuyVjNsfZpu9kfujUTy9gBIwxZB7kpz+Fcv835BKzFKQBU"
                  "DG4wh94dIVzYs+Xo1XruFZvltnBIVJu4rPFr5N0wLKfIwybUd5JryeDfGPsT55J4anOf1kAZBRFIciKEqg0cia2hX/WE1W"
                  "rYGEM1bd5I+8r0HBAY/kbmLGfp4bWrciPINyesnWADK++8JJQm+87D3VZNXZi23+jMKuYB0P5v4Yo5b5QDl1ZQGQUZScL1"
                  "H0vYSai/ri5TdxjDIKj4UvY9y+FqscTNuncAhkAZBxJib0BSrJCFbDnCGscuwyTmBL+EYaItQMzBqYE4gB4dSRBUBG8XhJ"
                  "jaLXVpLhH8z7yus8yVVt06h1TP0hUI5DZspcybawwNYAZgyaAMqpIwuAjBeH1fDa5c0Lb1/Ruvjb582+9BNr61d+cqx1/u"
                  "3ratd8NTbNskqiIByLjEJbSkxaS6RoNeWUkl0FyHhJKbjqy8+t3fDxghssgQM8ooa86zV5V71JiQEBlGOUERLG0kRXJNAW"
                  "8IAABhBOZ1kAGCynM0UJNX/WWfWr/6bgBkoQM58DQLDH1fwZgap/hqqv0JF1NGUtqZQRYoR9OLYQ6hSBtjgdZSMAOe139w"
                  "211v2nSrpsEJITfj9/RmHCbOL2/EMyY/qJJaQLjHpKvq0D7in63W2U/ScJ9DtZAJxGrIan2NkECgiCoHiOxmiwfLBz1uvA"
                  "c5JkJuwgh+LEMGOLMhNcxDN6EUX/87oq+TTrOr+G4eEsAE4Dgc+dUmFkNcRLiscRaI6jkxdFPt8HygslowDQNJE8nv8hJo"
                  "KXsKn1Hwj9n2YBcIprBtOcKkrpAAVfoSU1YtNA1GB9AIAgh5myiIBwqsgoMhH08p3Sh/Ti5giDyW9mAXAKE+QUPaJM8KSk"
                  "tg0oqSR4cQuO+lK4M7bN6SAt9oHnVJBRSAxyf+k39Ipam173gWwfwHHICIpSSgeIfIm868FLiusWXhzexLt25x/+ICggnE"
                  "qyEBDMPaXfomZehdUsAI5fRlH6khXkfBk1DsQjGAquSj2Y/N09+Yc/7cUpCKeKjELHhnJv6Y9IZAQkC4DMibts6SWVYtr3"
                  "ruWtCz8faWGTk47jFJNRZE9utWzJvQ+j2RrAc5MRNYi3qDh6k9GfXlu/8o8NBcADDlBOPRl5ovBvdCz+A2BHFgDPSUYwWB"
                  "/agc6aN3WbP+ZUllFkJqjKePg64A+zKcAxyygeRXGSkkpMYlpOkBwopz7l9Kc8JyowEdyaTQGOScZ3V/t7Q81fazW4eVl7"
                  "wxhQatvaRKD5IfDH2YCy+KbNCXSOs2GqBvIG9ntwp0rjCounUBRYZuEZz3MhM8FFWQAsWtb4qn5dX7LyJ6ud5W+upENrjV"
                  "qEADAHzfkdRzRi4FwDRdNtxt0pAGz1MKHglHmMwIDAJgtrQnhZDjan8B9mAXOUBlNAIBC4LoIfLcLL8jBs4Wen4SMNwHBo"
                  "CoGAocsKCAckCgld6Pz3Q1hIYUMAr8nDrMKMh2nXbeLdHlKFFND5f9Z8CheF8EdVODuEC8ZhwgHCsVOo20IWAEeV8eIKlW"
                  "TkfcvbF/z7UtrfBwZwgB5o+kVReHkEf9kPACKQKgA0FWoKMw6ELgUqBnoN9AiIAMADMfxaDZrMVwSujCCU7vcXDZwdwKtz"
                  "cFEEVnjWK/LdADiUHuAPq7AphKIc+DkKhi66wfWuGXgqhd/tgSZwfwr3xvBACujCJq55eGep27wAXqGhUFOYdDDpYY+DHa"
                  "4biLMOGgp1hSEDV0XwE0WoWgC4JIDbHMfNieEMIKrK6eLuwd/nVFFM+8j50kg1Xv63Q511t4ABUp6TqsDtg7Ax4rhNOLh0"
                  "HHY45qXFP/XBG0osyv0duGYCWixUAD7VDy8pcERvnoR/acHOZTBkAaDu4ZEU7mjDHSnM+W7dl0BLu038jSGIhEVTBREWeN"
                  "80/PcGIBwP7XVTMrNqIFsEPKSMFzc4EK/+zFBn/S2gQMpzNuPhl2fBK8etLFAQ5hP4gwb8cxMS5agGLBQNoCzQAn58Gp5M"
                  "OKwnEvhsB2KB7Y5nlQ28KIL39MA/9MPnB+EjVSgLIHBnDH/d4JiIcEgjFlCOj0AlneRwsgDI5vwDndV/0t85+3JIAeXEEP"
                  "h0G/65xXHTbi3wrRjeOAU3jcMzCUdUNhByeHs9/NIsKIf2/jloeKgKjFkOKVb4xwa8fhr2K8/6n3Voep6zActzof3J17I1"
                  "gFOMorzQFEc5GXzjsvZ5bzg5m3kE/lsNXluAnDDP5gT+pglbPMx6UEAVQoEbInhrCXoMmCPsSrw9ho804f29HFavASMcns"
                  "DXY9iewOpw4af/x9sA3cXFEcMCn2rB78zBnQldQpfAI921Al6cZ57tKXyqCRUDKyysDGDUQo/hkAYMiIByjARCjw7HH88C"
                  "4BQT+SIvKAVnksJIe/0vGM0DCSeedBfMbm/DzQXmeSqF/zo3v2lQgO6o4cNNuD4H+zwgHJrAPscRCbDawG4Ob9bBQ+nCAP"
                  "hqG1oKAryruDBI/rIOb5858iW+uxYGAHsd/PwcKIBAAKy1cFUIl0fw2vz8MFphIC/Q4pjp2uYXGYpvywLgFBx6v5C8eCJf"
                  "3FRNlr8IHCeN9/DleGEArA4AwwEK7yvDZgef6MD9CdwfA4YjKsvRA+BcC3dweNoNpAU+3wE8vLQArygwz/c68N5ZQDii7y"
                  "aH/kTvNzDpASAFnkq79dEW/HoNfrwAv1SBZQHHx6CDnXG/sfkevGgWAKeYnCvzQlJxFNO+W0NfBBwnjxx6kW21hfMtPJwA"
                  "wA8W4QN98PUWfKINSLeOpmpYSOc35rDlyAR2pszT8XBvAudG8MHq/GlE3cNPzcC0Hj0AtriFP09eIBLmkwPfN6Xwv+rw7R"
                  "i+PgRlOZ7mn3TXzLyBgnscJ5xisgDoi5fzQlI8kZYuBs9Jd18KLZ2/ol8wcHUEAvx4EX6+AgAVAwiLozAaME/dw/tr8Nu9"
                  "YOgaMsBRmnWbY55pDz9XhLeXYdQyzy/PdEcoCEfV1m7lhWd5Fm4u6jHws0X4sxZMKmDgngTeNws3R9DRxb1fADrausevbb"
                  "2DinuQRDgFZQFQdP28kBQl0KjISSewz3cbqmCZ5wO9UBCIDM+KhEXLCWy0zPMXDfi7FvxuL8/qtxzVQ+n8jBgN4Fd6WeDD"
                  "dfij5uJDqqPdynOABXqBJjBg4fIQfrUCl+fgCwlMxoB060NN+FgLvHBUIvgN9X/2q1tvkbqNSYVTVBYAonIq/AzC80GBhg"
                  "cs8/RaFigaMIDnKBT6LKwPeFaq8MEGOIWOh5wBgLMshAIJh9c8+iCBTzbh38yweAIt7VYv86cknxqAtsKa4OgBVVMWRRWz"
                  "PX+9jrZv0JH2bbgsAE5ZrWCWF5KqEmmhXUmHOelctwnmUbqE+aYceBZnlYWhgGc9ksCTKYxZ6Cjk6Fpjoae76AZy/LtIYo"
                  "UbIvhGzKKPQqtrtw4WyKF3SNY91DzPyVwwbB6s/IW7bupyjO5DsynAKWku2PuCXwUouN4tg511gOOkcsCsXxgKvzoDZdOd"
                  "/1cNx+ymEIQDvtUBp5AANYUeugYsVLoB8Jy8uQRvLMJn2/A/avD1+OghIN1alK0p7HeAcPwUGc+tkG2FX9JzGu8l5VSUBU"
                  "AjmOaFpOLx+C8qyb9/Xh7fJcyXaPcy28NJ97r/h6pwdR72+8V/ul6XZ57b2oB2G33aw3K6egz0G9jK4tU8PJnAiIUVAc8y"
                  "Aq8uwCvz3fWAX6nB1OFGFgq9pluL0VTocEKYrYU3uqHO75KacdAsALKNQAs5E99bDyf3VpJlo5A+v7fHe8ACSHcB7g1TcN"
                  "8I7E05OoVVFq7J8aw5D5MKl+YgLyDMd1kA98Ys2t0J/MA4VAM4y8K/LcGPlHiWFXhnBa7MwU9Mw4OHuSoQCoQLpzl8uQ1J"
                  "N5w4L4B1IawLukG1xwHCc9KwK2Q8Wo/VcVSyADjVdGyDF5bgJdk/FW3/eCVZ9nOcTBYoyRFGBQK7PfzHWYhZnJfmoM/wrI"
                  "LA5wahLGAAFeZZF3BEKfMJ0Ab2um59pzta4beqzHNxBF8chKvHYevCxqUgUJKFW4zfPE2XQtXA6wvwnvJBAQCg3cJwbBTp"
                  "GLQ/LjIQQ5oFwCnH+oAXmsEwE+76wxE79ba86yuB46QwsogbWgT+vAUhgHBUP1I8xCetHH7KsSHkiNYZEA5YJlAxUKMLgd"
                  "+rd+9ruDLHPKMWXpKDP2+yQJ+BwDDPDn9QYwvMAH/RhL9pgQEQQLsjg58swm80YO5YRgUC1oOTRNuWbCPQKciL41SQSOeJ"
                  "XYVH/tfZ9Wt/9eQ8x19hxMCgXdziWMJRKFwcwrURx6DbTFWBGQ7tnABkXuN2q3ZQ46XA3zQXBgBAyKFdGbLApGchgXj+cW"
                  "D8ZV/3vT7ehjscx0KLro5jp0yEnIKyAEilw6liIrf5t3vSkZuG2uuvhoQT7vIQSguHxoxYIOWYvasIecOznMLHmvDdGGY9"
                  "BAKvysPrizxrddCtmUPN1RVW2IW34PYawDHP9xIO6SHHIV0assC448gUfrPnQNAsMxwrHe58UwfiJ0mFM4Xh+GRUGjsLD7"
                  "5tLty5FUJOLIUrIhYQgWHLsdHuJ/9bywvv6X/bDPxhHf661d0N+KE680TSDaLDOT9cOKXYGLBAQ6HjmWfWww7HAr3mUP/v"
                  "R9hGrGAU/msF3tsDAAo8kHJMIodf3fwfOAHfrcPKAiAjCIp/cmvpnldP5jY/DAFgOSEiA6/Ic0hXhCyewpiFv+iDojBPSa"
                  "BqAANIt5724JnvlXkOqdfCJSELvL3IAu2Fm5p4MoF9DpCFB3uuCZhnj4MvdADtFr5bue50gU8OwK9VeVbTQ5NjILjz5v5M"
                  "e+OvgIL13TqSLAAyggH04S2lO2/aVrz7gx071zkQBAea69hod3Hs/IhDem0BKoZFqQj8Qx+cGx76k/aagHkdH7PQ9TlYaR"
                  "eeKHx2sLBRAW7Jwy05QI+8dvFQCm3PAm/Ogyyc+vDXfd+vfvhoH3x2CG4bhruH4M5heE2BefY76HhAFrXbyJ9T+6xf2/h3"
                  "eAHhQC1GtgaQhYCoTEzndv5MI5z6SDkZ+IlqMvaKvOtZZtTmAbUaiGBYFAv8YhmEQ1sZdOfzv187Sn777tl7L85zSAK8pw"
                  "Jf7EBCl7DQoIWX5+HPG8zzziJYYYFAujcsXb8f6kcIgM3pwt8csvBDBRaoGnhjkUWb89Dh8KyC9Wgl3ePOrn9Qh9q/j5MW"
                  "VjkO2QggIxgNUPzdc+Hen9uTf2zjYz1fvv6pyrfesK1078dUPCAcncIP5OGGHEf0X3rguhygHFYg8KYCR3RLHv57L0R0rb"
                  "dgWOgdRQ7Q7rrAjxY5rEui7vV5FADSbs1TV+bz8GMFGAl4zlJAlUMT3Ia5r6YvnnhNeuXk+TrY+Q28NFGemywAMoLBaojB"
                  "tDum/t2mnb59pH3OtUZzgHJUPQK/1gMiHJYDVOEtBY7ICfzvBtzZgWkHjkN7R+nAEP+WHId0VQ7eXAA8rLbwV/1Hn4b8Ug"
                  "U2hQdW8Pd75rkxghyAdmvAwvvKnBDLLOQNhyNNG2tv59MIUzjhOcimABkBQBAS6aCSEksTg2EgXv1fyunoGkg4OoWyBa+w"
                  "OwUF2gq7HTzjYXsCjyVwj4Oah+ZR9v4r8KEG/GUT+gxEAudbKAt4wABbuyvx7PNQ7u6sOyShO6y/K4b/VIGNATwawxMO9j"
                  "mo+26DpwoCWIEp3y0E5hSeSmF9yLNeV4RvWfhcGz7Rgt0OPtMB04H9DiYdKCBAv4WCgHZ/TQAMGxgSSIGcwIABD8x03xfD"
                  "4e+PsAoGCB0EArEFNAuAzPHcHJSAeDoyhxM37/iwSjp8DSiLI7Dbw82TB564kyhMe/CHanbh6AQ6wF534GTdQ1L4T70LFg"
                  "sXrD18oh9+Zqa7u2+vgzl/lJ9HeNbn2/ADBea5ItetX6h0nwfw3hloOMAs7pmBRQEHhHQDTIGmh5ZCKof+OzOKH2l9lLYB"
                  "JwCgCimn+vbf7MlAdw1+gFOLLjybrgsvjvVzNz7YH6+9ANLj/nNPvu5VB24b4oBu8BDTJUBFoCDwlqnuBiIMx6QIfH2w2/"
                  "CHM+HgbVPw2Q4gJ/DvTLplPG7j9Ef92bW344zjKMJPvygbAZxKCq73tDrBuBnMPNEfywUcM+F59a5it/m+2oYvxrAlhV0p"
                  "tA70Dv0GLPC4AwzHrKnw2kn4lUr31uABAxFQU9jhoKNQEbg86gbACfs7E7TanvUrW19C9Gt+RfPPEHEY5TSTjQDuHfgDTh"
                  "ceT84Xbz5v7qVfCXwe8Jyy1hhoK+z1zCcneFSiAJAXWGehIt3m36mcTFpwjeTF+14nof+yqiChZzHCf70qC4BTyf2DxxoA"
                  "CgigOFWU55eTlJH2uv+9pnHVz4HODwEEMIBjiTiFpzkGv7x2f3r5xJU4SVAWJfrM1VkAnEr+pfxbLJYgGAweD8BQmKNgAw"
                  "TwgFfleZIb7pz9B6OtTe+MfBHwgOAloW6nJkuu2mc1NJxcGask1+59LcX0U6iwGOEXsjWAU8r3GhMslsEQEpKSIhh6TEjJ"
                  "BqzOlyhZS48NcXi8clIZDTqT0fZ3tWztb3Ou8kPFtHd5O5ibaJm5f6mkQz9QTgd+lpMv4wwymXuZ72t/isRwGsoCIMQcYw"
                  "AYBIPB0PaOtlf2J9NEIqzJVViZz1OwBq+K5+SxGpJK55ve+m8GPqRtanRsncF49Q8aIgFPl+dkyQhmJrpEa2FEamLOLNk+"
                  "AIMgCAFCoilb2y3GOymjuYixQkjRBN0gQDkZBINR++xXo4a9+Sf+J8pF5XR4fWo6SdH1DIoGAsqJllFI7HKphWWcmeLMlW"
                  "0EMt0gwClsb3fY1WkxnAtYlS9QsBavz8etxCDoY9tL91/ncWtHOuf8f6Xmxa8Ez0mTsSiCksl2AoIA3RGB8ky7weZOjYuK"
                  "fSzPF/Cq6ElofAE6tk7b1jAYHC4pub7zlrU23cpJlBGwflrzaZvUsEAWAFkQxOp5tFFne9zg8vIAgRG86glr/lQ67M9tJp"
                  "EORg0KGEzf8ub5v281byDh5MloIXnE98SNbBEwC4AjrBPAdJLy7dlJNpVLLA/LpHic6nGHi5MELykeh6IYDAAqKdV4+U9X"
                  "kxXrIOVkynh8tXMvqYByeFkAZCxC7D2P1Ws8Y+oAXFrpIzKGVP0xbwYCPdzOut7hztk/AxZIOFkyglY6Nd/X/if8IgMgC4"
                  "AsBOo+IfYJBsP99RnOK1QZCop0NEV5bhRPzpeuriRDKyHlZMoI6dqZPyKXbsULmSwAjuFqgcFgGE9i2ukcZ0eW86JRFEWf"
                  "YwBEvvCik/2MwYzBLZ/9ph+t/85xf/pnAZAJEWJ13NPZRcvB9dEmPA7P8VGUUKNhTpKMQY3Dr5z+kltZezvOzGE8xy0LgI"
                  "xByBHwaLqTvOa5NtqI0+MbCyhKoFHECZdR8biB2gM61vxTHez8KU2bkuPEyAIgkyPgEbcdiYUXReegxxECCnic5wTLCKBo"
                  "tb3L97c/giMldBALpAZphmghQaMElOOTBUAmIuQxt5Mkibm0MIZHUdVjnALkJ+lwQmUUUUv49MgrnU5+JD1r6odpBZhGhK"
                  "u0kVTAA9qt45YFQCYi4Kl0nHZc54JS7zFNB7qLgKXbVRyiAaCcWBmZzp+PAl4glRP/wI8sADIRls2dOTrS4qJyLwqL2jSk"
                  "KKlJ7qoHk+OVZGwYUk6kjIKXqpkqvNsbvYvAP4TRFidaFgCZEGFHu0PgY5bnQwbCHKkqR+MkmZiMtn+skoy9hxMso5iZ/H"
                  "Jz/9gfaOCc72s9rML/xPq/5GTIAiALgX1xhx3JDC+qDDIYRiSqHIlRy0Ruy38f6Kx+UyUdG4OEEyzjQeLA2n09F9mJ8kfS"
                  "NVMvcitn3g2kZDCcMJkAIVXPPbUZJpKY0AigR3m5ndtL9/50x8wmJyuPMwp4cEKwuf+nZTb30xglAwEnVMYiOFXur82xvp"
                  "xnOIywYo64LjAX7Pv005Vvv3Vd/doP51xfERJAOdEyCmoItvW9L6m2/w6VyWwEcJJkIQD31Wo88P1qeUcgghxhKpCazt/v"
                  "KN730v25x7+nKBAs/uk/CIuVUZiNVtOxF5DzEOhh67hlI4CMABGGvUmbvTNN1uYqrM4XKVpBAa8LQ8DhvrOt9L0b58J9Pz"
                  "fYOetny+ngaqs5QAHPfAIYwONJ1GCFRcgoxkXEO9sbk/LM18VbDieXBcAJkd1arMqWdoupDozmcozlLYWFQYAgWA0bzWD6"
                  "97YG3/twNRl9fTGtvirvKy/Ou95eq2EACkAq7bgeTG+eDXd9Y6iz7kfK6VAPeBYjY0hq6epW3MGo5XmRBUB24pBTZVc7ZX"
                  "/HMZQzLMtbStbikAWjARU36SX9s/25zX8Wam6gEUytjHx5ragUEtOezLny01ajfbFpvL6U9v8UeBYv03Kxr6dNjAZZADw/"
                  "MgJYwKmyox2zs+MYzllWFEIqYhCE+QSrIYKZTKQ9KWLvFwyOmFq4D0VZ0bzwh4XQQMpiZRyJbT6Z2PYLOwLIFgGzEcHT7Q"
                  "Z3z86xN2kCjuCQQQCCmVeK4iQm58sDHIOMIbFN37G1BwThBZONADIChAjeG75T38OwnWNVMccKmycUyyEJpLaD4lFREtNq"
                  "cAwyAXPRrq8kpvmg8SGniCwAsiAwzLiY3bVZBoM5zsr3cJGMgHQwWAIRAjGkeEQNFgMYZsI9nx5pn3cTCKCcHgwggOP5FR"
                  "Db2WSy9Myve/EpJCxKFgAZ7b4QKIIMC1IVJARSQWqCjCs6pyjHyyIEGMbTJvvrdeKwgJqEQAM6SYcIz3DeEgBeFaOG2XDv"
                  "n+8tPPqa0damG8ED/hRfAfF0TK02F+59ciBefZnR8HkKroDE1nVn793/th3M3W7UgnCmyQJA570W/t6heJQc0aY8uWsioj"
                  "WCVASJBARQpZh6fMOR7vEUHnK4hxXdx3EKMCR4Hki2A0KOkJAIT4snOjEbSyVGojxOFY+v7Sg88AZR8+cDnbWvCzRPl6dL"
                  "uoUD9AVqfMFJTD3Yu69ppz8zk9v1v3OufMtQZ/1lkJ6U9+sydKU0w31bxsuP/mI92vfxM3DlPwsARQEtR4RrQ8I1IeGQxR"
                  "QADNIxmIkUuwPYo+huRQFFUdND6fVlKi83YBRiRT2QKgdYbMVi+3LkL3C4mQ6dB5q0b1N0z6ECRue/DrORKAAgxBIgeIS6"
                  "dzxYa7A8gnPLOUIxiDeTU7ltr5+Mtrx5MF77jkLaf3moUZ9gcCRxbBtPl9L+taEvFkB5/hiSoJ5sKd/9X53TbwQEm724vU"
                  "0zQ+RKrwPDieZMRz1e1KQk0plMbfPBWm7P5xvh1F8EGk2KWs4gWQAoCtBToPCSPLnLA+ygYCyoKiiAgIAIqHf4Zkq6o03n"
                  "gRR3d45oZQ+VWxVij7ojvI8DnKIYTKFI4YYcucsaNL7UpP1QRHR2SDBiMEVABEmAOWAvsNOjE4q2FeVIDAIIu+MOs7Mpqw"
                  "uW1bk8xgXaMrN/v61479+X0oG11WSsz2oojWCiNRltn9owd8t3Q19eAY7nj2W6d/NXZ3ue+Z3C5AoKrsyU3Y8IdGztQZU2"
                  "ogHgOTEsc7nddyn+Pc4k8fd/Pe2kszXUAqCIGs4gWQB4PHlyl1UovzEkHFY07pZXDqIH/dNgwhzRuRHRef+niT2+0f1vcC"
                  "ySok6haTBhhcpry5RfaTARqMwPnRwKqmgnJZ1wuCdjkjsTks2LuYzYcp776g2M5lhjK+QkRPAUyG0pkN8iGtAhwGBITKsJ"
                  "wvGzgAApiyNAzGxp+9/lgzxxocZjrX3MySznuDXUZPZT49GWb410zrsOYp47A1iM2mott/+u0BWxGqI4RA0gnEGyAPAoRX"
                  "Iv66XyQwAe3ziG5nUAAcEAMKhowqItHBUA4vFtDqLMY0LC0YhwZZ7ci2s0vj7L3CeAVFEUjRS1ijqPxgYFwCIIwoONOTbb"
                  "OUaCCsXAMxXXKfoJCpJjJKeIBtSjfZ/pj9e+l2MmIJ7HCnf8bSHu37gmXX8JeEA5MkOrsH+uU5j6kpqUiXCW6U4H60NyrT"
                  "Hqdt/GaZmibMfrJTdcfi4hoOJJTGOqEY3fu7/0xC8lpkU+7SXweRCOIBMs4ea/tJfKG+g2kTvOBk45MZQj84p6hQQwPVRe"
                  "AZiE5N4ihSsDgjWC5CBoG+wk6PYUt0XhKdA0RJh0LepOsR2hTpOAafJEPFULMLbNlZX0fw6Fa99SSEZHIGHxQmajzffvyj"
                  "3xtjmhp2Fqf7MpvuIVR19UNDQLk3cZY/fHzYD6bELRBEGvG3pHRH75xvjSH6n6kXMeLn7jY2Pp6rOG47OvOr6TOg2pabGj"
                  "9+4fU3GfT0wLUQMsuU/9LABKFBfbuLZE8RZAFHWcXrzHN8qUXqzoNRZb7AYRCkhItBr0co/GKekej/uWwu0GkgADQIAhxB"
                  "JgETVMpLF8YWbrjoncV3/qpf5VH4tcb3lxIRBSD/ZM7Sg+8I48QdpCph7J3fOTQ27krmG3euWRg8TTCqcfavp62vYBzkOH"
                  "2G2I17zy7OTC1xoADCs6G666p/CVf3Ourb1xeWf9uyKfN6AcYDhyMCihK2DUlBvhFEZDAJyJMWqXUghkAZAnz+JowWIHgY"
                  "TTkwIiiPX41oJFzS4JCVf0UX1rh84VMfHHFG0H2KEC+ZGAYCQkqBpMeYSBSJXwmfZcI7Ff+dSN5tpXV/1IBTzgDnO9Hlrh"
                  "+LYtpTt/vB5M3hf5CLUdBN3zaP7e3x5sjP2JOezmI0ElJbJRbVm6jinfYLPfjIrTlrT3GCwQA45BN3bWtY1Xf7xtmnusWg"
                  "HlgICZ/Pbd1uUqlWS4Ao6FFDAINg8ACgKJNEmlTeRKSyUEsgDo0GExuvNkU7PYPsBxOjr6eFj/36JmRHTOAH3/XlFvsT0G"
                  "EwJ60JWObhGx203v+Rf50scuNuddfa6u21CkJ0LtgbeSlFkZ37s3/8TfzsjM7wUSjxeIaIkjxWMJGA/2/NOE3f0rw271Kk"
                  "hYSBEN8GFcqA9vIZ3MMzA1xJyfpeJ7z2ceT1mrfWXX3wdClwMUUHaXH/3vQRxFlWT0dw699mBxpoWTeGug+Xkr/YoHEVSV"
                  "JSELgJjFUDS2mO/kyJ2laIclTtGOxRYBFE09PuEwQoJcR9PW7Xr/lx6WJ+8Zk+EVfaZ3NMBGHY0bE8zs283eh5qd+odnXG"
                  "u8pxORM0KbhOFChACJxJPboqe/PNxa/Q4OSyhOL3/1Lt35252Gne0JBZPyquVu7TWQMp+iJOwoPfr1jm3sXtXY9IacG4xi"
                  "O+lmc/u+Emruyf25x1861Dn3ZhDA02UA2J9/+nMNO/1d60IURxcIkFJHg5ScP2NGAtkioCC06XwrpHVekcLlHl9nyVAFkU"
                  "NecVgkgwkiTFDXzuzjum0K9H66BEQstpSj530lzNdn09Y/J6QxKCWTo5ozqIbsD/Z80knnHVYtoCyUUplbdd6yTudfdxae"
                  "/LuiK41d2Lnu5wpaMZAu2Ln39OB3Prw9evxnqp1lyeO9d3x0ZeP8D9Vz+x5shDMPVNJBJqPtP1gLJ351oLP6hwuutx/UN4"
                  "PZ2ZaZ+dfx3FO/7kjaThyHpuQ47WUB4HAslsEkDRp/JYgpkL/I49uAcnpTEROo4kGV58higv9TgNCldClo3EPlpQG2Ms3s"
                  "Rxwa72zXGbHLKYsBzOM1M9WputEcpByKAGOdc28Yjc+6wagBLAu/19Io7do1WX3qF4J6lAQuwtn4C/f1f/aSghY6RgMEMG"
                  "rn6uH4L8+Gu38dYZXiXeSKuwqu2jIa4BEEYQnLzgPwi3w5HAaDYOoNGn8yx9xX6BJOYwq6MlxzZYi1evQA0Oe43qAeXy9R"
                  "vOr79XKh+2qmnkhzeNxMU5q7QY56HPeB1XjHQoa50u5v9EjP7HCphyCnoAZgCqTBQbphIC3FPaH4pwXTMmo5fhmzhLf/Vn"
                  "NEP9hD5Rdy5M9WNOE05vE+Z6LiRbrh/EhyFY9POSKxnAAebZUp3ZQjGg4I2e9qtEyDljQ7Hl9/7uuZStPUH64xR0PqtEsT"
                  "pEEbUXNCT0IOFKwKS1y2BuBRIqI1ffT8VEg01m183IFr6acnRdMS5YHRdDC3xqzedI+7b4fFhsyH4l3OFKvVoP+cffHOOw"
                  "WTA5TjpKiz2J6Q4Ow6zfGAPAUKKJIzmBLHzAKGLgdAEPlGPi8YDyKeRDpQB4ti1RN4xSjHRejalReqaUrOg4pymssCwGAQ"
                  "BEUxGBQFIECqA/T9VEg4vJQW/zze5SXXg4dL/fkX7rJ7tu5ze5/IkStxEId3Va30rWbF2t1s/06A4bkSRBTKCQleIXAROa"
                  "QSajQMyuKFtOxUZ2vxoY/mfWnZ6saFr4qDmkttZwIEAAWiXEKu7XiqXGG20EvoAi7b7SklkFoWzahiFB7pLfFwj1BNY/qS"
                  "Il5YlPVZAJy65KCXwRASoEBIcE1IONZt/iVHQMlrzryMG15xm/0me78fAhFhQRADiEd9r+npX5UO994lNq+qXhDhOVEPOh"
                  "cS0pI6T/AkZd/bV/G9ZfCLPgVxuvTMo4+W7nyXd/JtNa4wYyffKvn4ES3sv8N6iwKheiZtnkcGBpnKFfGieFG+sdrz4u2G"
                  "UgIdu7jmT8Wwp1BlezEk7zu0rKFhhSUkmwIIAEpKSkSEAIp6lhiDsW3tzHrxGIVeV8n9gHnJa78T3HPnE+7Ju0RJLTYHaF"
                  "GK/VXtLfaa6ui0m9wWEOQ4ToIEDjebkDwTELAi6iWwSh+D1+a1BPhF3hb85B37Sk++MdH2rlzai9O4VQsnP1TVKh4BIFDP"
                  "lM1xd26IjlgC9Tg8VqEZCt9ZmefSPS2qbfCiHE6gykwY8Gipn6KvEOgsMWAUDMoSlC0CpnhiEmo07k1J9wliWUIEsbM6Oz"
                  "5lZttgAUfeR3Kzu+bql9ob39Rjq6MpaUfAlChVjM9zPusvU/S55qut0fhqm3gisA4fNGnZOQb88A1gObqAes+2zXvH7nmT"
                  "LzR3iRq6mHckd0i3+e/KDRNjCNRzsMBDM/TcvqqH+0crzOYCRJXAQ+iV4P+Wx+CZtRE7cmO0rcGqsoRlAaAoCuU80VVlij"
                  "8zyMDPWmxBUb/0RgDt2ma2Pw2GLg/qWZeeNfYabn3zqmDVJi/qy1ooQMp6PXvtSDB6dorrcJwUTRy+HhER+hyKwWg4uCxZ"
                  "cQVHJXjTYd/oA+9L87WdSWkWjyLMZ1GmTI67u82PRQ95LdMooMK23oi7VvTy5bNCHhuM2dETsqOSZ7xUZE84wubCKInIUm"
                  "/+LAAUyJG7ro/eX67S+1MF8pcG2CEgBJQlJsAGj+gTd0+bqTYEdCmQUHYFey1X3Jg3xb6cDw14Qh9xoWy8EsFwfBTQfqo/"
                  "1kP5bamSq7kOva7vqn4/vArc0Y/g7t12Ryua/pTtFAnTAkO9EbbUwSsACKACTwU9tMXOa36jMmaQfi86/wRlrzgj1CPDHc"
                  "s6fGcs5K6RCg8MDpIwBICgLGHZGoBHgyqVt5QoXq9oqmhTWdoMJmj5xtQ37F1ffZW55ZWhDwBHV0rVVXKj4eh68eIBIGW1"
                  "Gxur2r5ls+n0bouNOHaqaFyieAOQn+nMfPBqc/bbAi0CMUeW0KyMf7EQ9zvjLQAikI8UHzeIY0VUaYll3OYJ1c1LHkBWzf"
                  "X+yu7S3Ptjm86KCl0gCgIsr45hjOCs0rPdYbxDBYQlKwsAReke1Fm8yeHrgHKGCAnzu9yuR74WfKdyM9deF3h7IARUGDQD"
                  "yxRVAFAijRiR4VVTTO6wWI6Tenw9T/6CyFffudqdcxN4jkwAJY0aOwlSVD0ACgQilIyQjoMVZY/0ELoQo4oAThSPxxvdVU"
                  "py7tyZof/8wODu94XecIASEFDKlcGCs1DQFmibJSwLAEWJiM4qU7rJoQ1AOcNEhIWn0qfvSoM0vo6rbqz4ioUUgGVuaMDY"
                  "ICJVAFDDoK/2I2JQnpOEpH6ZXvTuXh3sh5QjM8TRbKcdNO72EiMIB4tCT7vH8GCuxB5rCDyAIIDHo6IoytbK1Ed/8Jnzb9"
                  "9brP9DM0i+a1QAcHhWyQhGI+raRNWgKEtYFgBFiihKjugSg4k8vskZKiLMb0233jtlZ/ZdZDe+aDUr1vS4ol2VDvd5FPB0"
                  "QVEKZRGxqCqIcBwcPumV0sgFbFgPytEZ9hWe/vy+1v6HAh8d8lLd1uoKZqKAyHnmg7ZJqcZ58j7crKL+somVv/btlbteHT"
                  "nrFSUyQjWoMuNTsJwJsgAokAfAYkYU9ZyZBFBQDQnydTe391tyx6fuNoXyDeHVr16XrB21JBygGGxoMEYBYT5FvYAcJRjU"
                  "49ylXHB9SashJByZoKbNdO+Wv/HG4STmYBbPlmiQui0SOWU+UBgJvakPt8qNcpzTpk12nzcx/MrvLRu/qBUm90kKdriE1A"
                  "Mg4QyRBYDHA2AQBQxnFnW41OFTQUTERIKIVwX1SdPV9j9unnlonawaRQXQefcHKOpBLAeIw3WshEWLiNM0PkwIaIe4uUnW"
                  "XXeeblgLKUdnqZd3bjbF5HND2j8vdgwwZ2BrrkxKfcHGHAXOro/8VhzJ/1b8/bWgLUalUEgLrJgrv+Pe0b3vDlTIB0VEOJ"
                  "NkAdCkiaIEhN+LiK4QJDxwk8/S5UhjJ6q90jM8apatG9WhsaqWi4Ixc7bR3MXu7Vvd9od2uB2PTJjpawddfxEcXUKDZs2r"
                  "cwFhcNB8vtVrqssutZfceo+79/MNjVsGGzAfKWmyway9+jp/zTWCsNjFv7ne7f9gcmnLuvlXZAM8M1oh6hQp45lHQUWXnz"
                  "c98vJt/fU/3ZzfS802em7ac84AKOdO9d/42MBEMUfYNOU8OqMshrJEZAeCeABi4u/OUustUXiJxRYBYYlSUT9khs+6gI1X"
                  "rNUVy8M0P68Jl3sZOE/OWTlu9l/0Fb792cfM0w9f5666EhwAiGePTOwTxR/U/M0hO3zOy/WmV8Y+1iatOcEY5sPj07IU+6"
                  "7VK64PiICUoxMS00gmzJ7bfF0QdRzMoLQDsEYQFQ7mxDPYKl0x2C6u2J027AAFKt5e2tvJV8DT385vWDPZs6G9PLp3pmiJ"
                  "rRtOA50WSJRDc+IxyDqBXUCL01cWACkpAHnytGh9uU37wRLFV3y/Ll6Km38UdUVbWTEoQ2trrjaxWXboGjO2IufzgONZCs"
                  "NusPwD5ubX32EefLBp60nRFUIQZk0t3u12P22xEXSbf9Qu2/gyveHWsq8GT9jHtiaatCOCiPnwqBmif21BK0DK4hjahZk9"
                  "ndzcnaKGgwlKgmVrEBFLi5j5YuNYU+/fONyssL3yTH6GGudOVS8K1RpQejq5YMa2BmeGPet2D71z45M9v7FnoPGNR9e23y"
                  "5KE1UO1jEpfXHp7UUXveiR6t53GwxLQLYPwGBsgfwNRQrXBwR9ghhFlSVGENtOG3se5dHtHucQYcgMrb3JXPPSIT/YM78p"
                  "Uyq+J7zEnXd+zbR90RVIxendcv8dLdeYCgkLMXFrxI6uf7ne+IqSL1gkYdxMTeF8CuQABRAkAKKY+OGWaaTq3I3C4rmwVZ"
                  "fAt0RZEAAWob9dJCVA0AUBUI0Ll1gN6YlzK7cXW/TEo2cbDQBH4C1ROV9cN9v387d+Y/B/5eKQ/gl50z0rdrx/2jQeKtRy"
                  "RCaHEw/Qc3Z96D++aGL1+z6z/KGX5NIgsSqcxrIAUBSDKRfJvz1P/hJFY0VTRZUlSlECbAg2RGHC7d/8GfPlj99qb3r9Mj"
                  "faCwkHpAyl1VwqKQCx6bhdsnerxdqEpN1n+1e8TG94ZckXLaSAYYqZfQZjAKXLJCR7Y9LvtOl8Y6t92myTp69bk553BSQs"
                  "RhiXKoEGJdQ0OIjBYwjoi4t4DQDlYIlxFJNoDISednTJgCn+9XC7cinIs8P5DbOD7zn/sYEX52ILeIwaoqbYvpYlkZTEBN"
                  "WepPBDm+bG3rNhbuX53+t/6vMzYfNrlTjiNJcFgMWG/VTfnid3qcfXOQOFhMW2b0590X79k68yL3njkB8szW9MJVALKEWK"
                  "wYgMLd/M03tzpli9hete2eN7QkgAQ8003Yyb2WMwAV0YJExIdswwd1veBBQDQyNp7AFhcTz5Tu9YxQ1c40x8G8iBub+P2B"
                  "5bWi6l3+fxeA5mRQi9iQBWz/XcvDucWtHXKa4BBcAgXPHMyA0AoIBhotzc25qtJZu2DdyoVn50Y230Zf1xZXXkczRtwz3Y"
                  "u+u3QmcR5XSXBUCO3JV58pd0m/+MpQFBvunqE5+3X/3kK+zNPzjkhrohgHKAgjOMmMFlT5gn06vNhTeNpCM9ENNlGJfJ8a"
                  "Y25yxi6cKjnSLFazokO1Ti28pSXDnixq4Dz+Io1hVt2Oq5aq769G2BDzEC4HikPsRMXKRMm5oYROZvP0jEEUvaBs+G6aEL"
                  "p8PmB4s+lwcPgCgL/h9tjH3p5nP+eUW9uqHkioAHFFAe6N3+mTnbuD3nQxTPaS97NmDhMkUdGQ0JC3VX2/dZc9s/XRdcde"
                  "vZbvUoKoDjAE+P6ekbZvis89NzzoGULgFRnpFtT6h3iRAGzJeWKF5Xl/Ztg37kTYN+tA9SFkcBS6k+8pJ6NPk7xgfpXKI0"
                  "GkWaOQgDB6nBRAF7zQzieVZsUwbbpaeBFxuFa/eteZXKkQ8UHav3DkHfEHggpcsyE87F9/ds/w28kKpjCcgCYN6jvjIaEu"
                  "TbvjX9Zb7+T5vt2Zds1HMvGPF9vQaDAKJKjy9XN3He1ZHm5eAG2WP3zW5z2x49zGlBXkB6g6hvfbzpx8EAjsVz5OLKhnYw"
                  "XdjdkNrU1CCjWsDkWjhAnWe4fxnbqTEzs5/AhiiQmJQ9udk7VNK3iQqgiC4mcNyCfQjf6n/y9yfD+r05HxALS0R2FcBzsI"
                  "xabKhe9Sn/1J1bZesDvaa63IgN1pm1F1wcb1jd7yrFHkprwNFliU2sd3DP11OftA4OAIdPPM4bTOQN9dWy7h0r/OqLjj1z"
                  "FZsWwvpcNdzWmaXHeMQrB1OUc9dewCMP3YVLEkQMgTdMhHP31Gyr05OWcqAcGwEM36k+8blHSrveb7whxbN0ZE8Gmg0IVj"
                  "JPRhAJCfKq3k25ic0dOvVKUOqF81YH3hBgAQUszni+Ye/81p5kz1MRYR7QhDQWkB5TGRljdPUyGV47pP2VSrtSDjQ8jtxV"
                  "ckm5d3D/JV88O9r5qWk78+0U97VUHIIBwHtPT6nKyNAKntn+OGEYggpTtnHvM4Xxey+pnX01eBbPAMJdvU9+9cv9j75F0Z"
                  "ZVwxKSBUBC+kye/EWKslBGEGOxUURUbmlrRsUjevCR3C3/TXPn159Kn74nR1RwuMSLMibD557H+ktW6dhYQUsG5KDFNM+x"
                  "U6wPzSZ/zuWb0nWX10yNvXb/9+Jk95/uDeofC0QaAEkas2bVelKXsmvPNowIoVq9r7z9f11YX3n1gecOSrfwLCSApW06PF"
                  "Ta9lf3VLb9jBPfCtWyxGRHgrXp3O9wDcByRFkQNGjMtGwHMLQljh8IHnvin+WzH30yeerunEaFhKRdlELfzXLtD71Gb331"
                  "en/uioIWDKRAAjjAc/wUSICUii9xTnLW5a+ZvPpPb5zadHs5zb0yNR4AVWXV2FnkrEMlxruUrcHej3+r+sQnwABCO0j8ZF"
                  "RrQgBYwHSLgFQ8TxZ2PfF3w7f/6BPFPW8r+LAlKixJWQC0dzVoftNgjrD/P+Nwnbo0Gy1px2CpBw03Feyr9ZrCUNkWB1vS"
                  "ro2a0XNfIy9/8wZ/3iqjAiSA5+TwQIpR2NBYedGtMxf/a6kTvs+JoiihNwyGbdaGAQP9y+gdXpb6UjQNAMI3xp754N+suO"
                  "Pa+0pPf302qM3O2Wa8P5wZ/27PU1/7xNDdb/9a3yNXztnW3x37p34mOA0f+/3pgKBaoHANaKpoDCgZFPWpuGTMjmy8kI2X"
                  "9abFCFIGk77CTen1l4MyGUw0n7Dbnrgw3XB+2VdCiHn+KJBS8qXg4qdyH3i8J2Zmbfj7+6eeIvEJgxqSt72M94WbLn1s5Y"
                  "+AYWtl75YHBvb8mp1z++8tbbnpm72Pbyi4aKAdpJtH0p49+6IaPUmexDiWvuwqAIJ0mjQ/nJI+GhFeERKsMticonqmN78X"
                  "r5fY8196pb/kQusjID2QjeoAGEiGitfI8CWoA1JeGJ4wNZz7YO79D47K12cbu76X0CE2MQP1JOh1fT9VbRaKicT61WVbf7"
                  "Vl/P68DQmdhYDHAQQhUEughjNIFgAOh4DOMvedIoXdVXp+FhBAOXOpw7nLzUUvv8JdthH1QMKhOVBOCbmWzfVtbf9kQ+e+"
                  "t6wz/Pa18VlvHepUV/W3qqvA8ODI1i/NLNvx9z0YgkiR2SrqhTNUFgABAYqiQEjYW6H8DoPtVTTmDJaQdNaYlZdc7i/uNj"
                  "+e04PBTU5dvqGz/CM3TFzztkDzBy0+Kn1GlvUPTQ2DjouBTqmJeaQfdcIZLDsPQFF66XlJjmilw9fP9KF/KGHxMi64SvR0"
                  "OyMvZc3e/svXp9deDgEQc0DKWbvXXbhz6853P73qmf8cxCFRjyNcX6P1RBVVzjRZAESEAHi0kCd3oUc7nOFSXLxCRteP+O"
                  "ESJJxucmmOLsdCwvJ9y1/TyXfeH6RBB8BYpT1oeWqyg/eACmeQ7FhwAIWqxVSzG4NAUR1laDlYIOX0oxyep7dZGV25d0XO"
                  "etOxLsAZh8vF9JZixsMYlRRNItQbJLGIcSxRWQAYDACKGhAhAyAFzedYkhTjrImSCOsN+wf248TxxFlPEWBweIri0b1lcr"
                  "EhpU2nZjAdQYSlJguANm0AFK1FhM2AoFdRz5nNz5lGE6csPUIaJmmr0NKZ3mm2Ld/O0MQgzjocDgEEQVbOkQNiUcLYsDyx"
                  "ICw92bHgLQAUnSuQ3xISXqFoyhnM4eLduneLJ73IICwtwmzP7PY9o7tr9UIDFIw3iArzpAalyxiQnGdpys4DAEBRWnRuL1"
                  "C47EzdA6Codzi30oxdPEDf8ra0fVGLBpSlQ8l38tWeuZ6/KDZLExPVic+kNv0mR6KgLFZGVJXTxW/I+wAQBI+XPqrvKlG8"
                  "4kx5RqCCAgjgcO5is+klV+pl5xu1QMrSZAABhHauxSPrH/zj+zc++O+ssykn2dv+8VeyADiV/Lr8Al2gKCHB4AD97w0Ihh"
                  "VtsQR5fOJwTsEaEQuQaNocNP1r3qyv/mGrEeA4MwQ4m/CFGz7/ln0D+z8WOMvJ9NaP/1I2BThVCUJCOjHL3J/00vMTAcFa"
                  "IFU0AXQJNH7q8L4ipeExGVkzokPLCpLvBZiW2b0xiRoM4DlzpFgXsXb72rcFSfixwAWcUbIAWEhhxwyzvx8RXZsnd2VIuF"
                  "yQvIAo4kEdoIoqoHQpp7CUtFOS4uDFsunadbp2bVGLFrWgdMGgSozombj84RmaHjwrSiIx3ihntiwABFBot2l/JSH9poGx"
                  "kOicALtcMEMW6TWYIkgkiBXE0IWiyanY/L2mZ8XLuOG1g34kDymgQMLBRA2gnIm8KM46VJTnJhOwRAiCQZKUdJvBb+vQIS"
                  "GViLAUEeUFierUQ8HkQE2Z8nUlitd4fONU6SRFXShB6WaueVW3+WMOTznzCBCwbXT7N7aNbdcgDTiZzuGGLABOxyCQZ7+K"
                  "ClIXpA4QkyAICiTMbDWYoEDuckAVEsArqnSJIALI87TXQBKS+HzZcO2oX14+VPNnDDv7tmx+dPXjv9nJx5CSyQJg8eTZF9"
                  "CdNnywSeuSAvkrQsLlFqmAhIAA3uHaQGqxA6CpgjuO97SCBB7fOdqnfyBB8Vw96xxQ5stAwL7S7r2fPvuLr0lqydagLvQM"
                  "hRgDKJksAI6dINqhfa9B7m3Tzqe4vgBbFsQqGscksx6flindUqZ4vcFUFDyQKuoA5dBEkECQMCHZ2yZ+stTdtHTYibvHu7"
                  "KUBnqp9KKe+TLg6G8NDqydXPWWh/WxXzUmJBeCsVkAZAFwAkYFirYV3aMoAAd/bdL8RIfOHQUKFwmyLiJcZrAVi0QKhm4B"
                  "KOAVjROSfR3ihxs0vxYQ1IrkzjPYHkUdC6GgRfLFnEaAMl8GlNBH4bW7XvSL23XfJ/ouaH8vykPS4eTLAiALCUX3xCR72n"
                  "Qoki+1aPeEBIMhQZ/BFgQRxacJbiYl3WuxEwlx22Aoki8p6gA5yvsYQTicjKMS9wYD9eqLqW77nmoRVSWTBcDzeaUBQRop"
                  "aQPYIwgBgiA4PGn3RUAACDlyeNQrKIehqArQptPqSEJBAw717RkFDJVyEOQHC+uaHbe3UJS6CBgRMlkAvAALikIXyLzfB4"
                  "+nSQuPb/dQfrSHysscWmMeIbJBsePiuTlfn6ybRrNAqQie+TIgeBI25ldd29we9rWHZn+t6RJm2wm7ZhJSByKcGrIAyCiK"
                  "w6N4bdL6dI7ciojoPMU3FTyAoj4IbG6wd+iiXfV9Dz6WPPXwEMNXslAGxSCsePyi1xGOrkL2/9evTD+Ny7WYnUvoJGCEU0"
                  "cWABk5MF6o1Wj8SUjn1WWKVxlMSSEBTZtxe2JT7qyLLy6e95a72g9+azaeuqjX9+cg5cwldCmKIggeheHm3now7mqbnnn/"
                  "zIx32rC9lPyssWD9qT0CyB4Nlqm1aH1shrkPzFH/bEKyG1ArprQyXn7OitrqoZuDq185V5yeSU3LgXCmioO290ECGJxxqC"
                  "ggzK3Z+/mZNXu++ZXtO0mf6Pnksvrwt8MkfBcQcXrIAiC7osCOBs1P1Gj8t/1MfmDGz/3VfaUHfm/3ss3jvXFvvpr0VUQw"
                  "oJx5LHXbcJ8wn/uHf7Sf+svNPU/uEBFaUSMxAr0PrHm72dV7y3lPb/z/oqKPJ8f2vNIX0rsEU+Z0kU0BMgaDx3dS0u0pbv"
                  "s97tHb4031B185s/LvK/XhIsSA58zjKWherpcrbki9T6vNgd4d0Y6tj/Q8+PmXT9/6jqBTzK3Yvna4N6jz0RWfeU1hTnYM"
                  "9aY7hNNGNgLIKB5Phw6K4nE9bsaMPHnv3s/d0XPvZ7esfuKpudxsAsqZR7E+MGPJyrFKpXe0Rys9y92ykRtq1785SKJc2l"
                  "ubezh8/KnHo+1PT9bjp7dMNakn6elyGTAbAWQEhyMlRRAAAgKxyGBnv9/weG7b5q0D07O36BXLewhCcJx5FIcinYJ4dYRx"
                  "vhDGxQLGof1x0/Xv/W+PTozftc4MxeKVErPsSVu0U48Ip50sADKzMclsiaKd7sw8Vpny1+3v271mZP/gdXjOSNYL1UYuBK"
                  "VbDrwQbu0bvejiVevOv774EZx4EFppldHcDF7JZAFwOh9x5l05F42/9FVjHx/dW76Vca5b7KWypUmZT0A9aKy2Yy8kdPej"
                  "SjkMuWJshNNWFgCZFM+Lzh/m2ivWUOo1wrbCEHqEM/8C7ynFjk4Q0g4BZWkzMNiss6x+J33xPxAkD+CELgXnOW1li4AZBS"
                  "67dJjSiAGTKJfv+UUu2PsFQu9AmM9AX3tcX/HMW/StD27gkj1fA2GpUoTOpfu+y488dhHX7HopkX8AFZaEbASQUZRiFAIC"
                  "sUJqIPJPce3OH2VHZSczuSKk84fF+0uj8t2xX6fafoh95TUsYYKS21Ua4L7h/8y62fcS+GlSC4HjtA+CLAAyMZ4L14wyMN"
                  "ALrRSwAGB9g8v2fkh3lW+R3eVzaYV5UgOb9t3OupmPayN4udy1/E3MlQDAJqBe8UZYalKzCqFEbD2qUFbwFoTTXxYAGVUF"
                  "ZT4lZqz2XqoNoxfvuVy2V6+iEb2WfeVLsdqRhwdvxkUwOjv+TLD5C0b6rh6dHllbqNsAlCWlFlqeqd7CTP6vuWD/76ByJ0"
                  "5Y2rIAyKQGnPHk/N0Id3PF7s/yyPCvMhMt4/z9n6THTH6vde+Hn35M3vCq5LwVuSQIQFlyYivsrvSzu+81eNawon4RznBm"
                  "yAIgo4AX1OozvGjXT4ozYIX90w0+9dcPRjdFr/jjSlIuoK2lu1YdpjAyt49zpj9IXxuccGbJAiCjQGwhNWANaQsSdcmj7q"
                  "E/2hCu/aNlcW8OUkAAPc33D0i3ltV2s2H6U5TjfyXyDzNW30lHICSTBQCQHVSm4+meD/+9fPqJ1/Tf8Oej8dj6tNhp9o5H"
                  "RQ4llyaEPqEeFjllGYhSOH/fJ7lg8t04uwsvMJcDJ9nqf7YPIINCYIW+SoHRaoVbbhj89vKLG3eXYkfPTFDkkAyM1fezYf"
                  "JREE49tlvD9Zpes+3dXDT+Q8R2F6mZN+TPZCOATOoYHCzw3ndcgwCmYGF/5zd1fHJINve9hDgIAMBzgIctvWP/t46bHH6r"
                  "Lnp8w3wA62Dj+H3k0u+yavJDdIJ7iS1HkMlGABlrBWMETRzqeYoVtVfoSzZfx8V77mZsbg4EMICFaqfOjdu/yg3b/5DVM4"
                  "8caEALCEcmYBQGWm2q7ZiDWfX0tWYIfMqiGCCAameOq3f9K8ONFlft+RCX7ruedTPvwsm9eOEoMlkAZFS79azYQjG5k037"
                  "b9BrdryY9RMPs2J2kr5mylyuzD2jV7C7cj31aAwsjDTG9cLdtxGlQAgIIAseyslofZJbt/0CL9+6hldvXs1NOz8FFrDQ35"
                  "7ilh2/zXBrNwiAAp5DElg+t4cX7fonbt7xi3rBxOtYM3Mua2Z/mratkxiei0wWABkv0LFtrH+IK3ffwJV7LuWqXdfxoj1/"
                  "yZV7/oiezgMYrbFx/Fu89qlXcOOOlz06dt/PbSvu3NLsi/G5FLCA4MoxDNXGOX//bzDS+mfuH/5Hbh/7BI8MXMpQfS9nTe"
                  "1EGeRza3+P3eVVYGDt3A5u2fEF8i6ZFybWw9U7Psb1O6/k5u1vYqj1p7QDSM1OUsOJlMnWADIqkNgpYjuFYTt97TvpbaP5"
                  "FM7fOygmmMAq0s4xpbv++K7+Hf949Vk3rDs7afY8WG/cvL2yIrq0Z/pfVpTq28jLNmq59/HoyPXYFPDwpif/LYVkK58761"
                  "8ppjU2Tn2H7ZVL2Nazin3FVbQtoPPn+wX/LWrRTtrB87awl8kCIKOAE3Cm+zWxExgDkQBgMIQaTJjETEguYSI3/aXtAyNc"
                  "ECsADHZgiru5bvtf0d/5ElPRaxHGMfJZLpq4gVDnaJuHWFFfw1T+N3i0/1ZgiGYIGLAORhv7WV27j0DBcUrKAiCTUcF6S5"
                  "gKonQ5gZ74m2yY/iatEIrxx6h2oB2AcjteIDEgupVzZ97KBZPD7ChcRS1/GV76MbqVs2c+TSl+Ei//f3t3SAAAAAJB7KF/"
                  "ZyhAAMTWAHMC8w+OpI5xRcATEBAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQ"
                  "AEABAAQAAAAQAEABAAQAAAAQAEAFhK0Bk2qwYZeAAAAABJRU5ErkJggg==")

HTML = str('<script>\n'
           '    // start data\n'
           '    let data = %s;\n'
           '    // end data\n'
           '</script>\n'
           '\n'
           '<!DOCTYPE HTML>\n'
           '<html lang="ru">\n'
           '    <head>\n'
           '        <meta charset="utf-8"/>\n'
           '        <title>Список %s</title>\n'
           '        <meta name="description" content="Список %s"/>\n'
           '        <meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
           '        <script>\n'
           '            (function icon() {\n'
           '                let head = document.querySelector("head");\n'
           '                let link = document.createElement("link");\n'
           '                link.setAttribute("rel", "icon");\n'
           '                link.setAttribute("href", "data:image/png;base64, " + data["1"]["img"]);\n'
           '                link.setAttribute("type", "image/png");\n'
           '                head.appendChild(link);\n'
           '            })();\n'
           '        </script>\n'
           '        <style>\n'
           '            th, td {\n'
           '                border-width: 3px;\n'
           '                border-style: solid;\n'
           '                border-color: #673ab7;\n'
           '            }\n'
           '            \n'
           '            img {\n'
           '                height: 150px;\n'
           '            }\n'
           '            \n'
           '            table {\n'
           '                margin: auto;\n'
           '            }\n'
           '            \n'
           '            #background {\n'
           '                background: #000 url("data:image/png;base64, %s") center;\n'
           '                position: fixed;\n'
           '                z-index: 1;\n'
           '                left: 0;\n'
           '                top: 0;\n'
           '                right: 0;\n'
           '                bottom: 0;\n'
           '                filter: blur(10px);\n'
           '                background-size: cover;\n'
           '            }\n'
           '            \n'
           '            #content, tbody {\n'
           '                position: relative;\n'
           '                z-index: 2;\n'
           '                text-align: center;\n'
           '                color: #000000;\n'
           '                font-size: 20px;\n'
           '                font-weight: bold;\n'
           '                text-shadow: #ffffff 3px 3px 5px, #ffffff -3px -3px 5px, #ffffff 3px -3px 5px, #ffffff -3px 3px 5px;\n'
           '            }\n'
           '            \n'
           '            #zoom {\n'
           '                display: none;\n'
           '                position: fixed;\n'
           '                z-index: 3;\n'
           '            }\n'
           '            \n'
           '            input {\n'
           '                width: 100%s;\n'
           '                height: 25px;\n'
           '                background-color: transparent;\n'
           '                color: white;\n'
           '                border: 0 transparent;\n'
           '            }\n'
           '        </style>\n'
           '        <script>\n'
           '            function zoom_in (event) {\n'
           '                let zoom = document.getElementById("zoom");\n'
           '                zoom.style.display = "block";\n'
           '                zoom.style.top = (event.y - (event["srcElement"]["naturalHeight"] / 2)).toString();\n'
           '                zoom.style.left = event.x + 50;\n'
           '                zoom.style.width = event["srcElement"]["naturalWidth"].toString();\n'
           '                zoom.style.height = event["srcElement"]["naturalHeight"].toString();\n'
           '                zoom.style.background = "url(\\"" + event["srcElement"]["currentSrc"] + "\\")";\n'
           '            }\n'
           '            \n'
           '            function zoom_out() {\n'
           '                document.getElementById("zoom").style.display = "none";\n'
           '            }\n'
           '            \n'
           '            function create_table(search) {\n'
           '                let tbody = document.querySelector("tbody");\n'
           '                tbody.innerHTML = "";\n'
           '                for (let item in data) {\n'
           '                    if (typeof search != "undefined" && search !== "") {\n'
           '                        let text = "";\n'
           '                        let i = 1;\n'
           '                        for (let param in data[item]) {\n'
           '                            if (i !== 1) {\n'
           '                                text += data[item][param]\n'
           '                            }\n'
           '                            i++;\n'
           '                        }\n'
           '                        if (!(text.toLowerCase().includes(search.toLowerCase()))) {\n'
           '                            continue;\n'
           '                        }\n'
           '                    }\n'
           '                    let tr = document.createElement("tr");\n'
           '                    let td = document.createElement("td");\n'
           '                    td.textContent = item;\n'
           '                    tr.appendChild(td);\n'
           '                    let i = 1;\n'
           '                    for (let param in data[item]) {\n'
           '                        let td = document.createElement("td");\n'
           '                        if (i === 1) {\n'
           '                            let img = document.createElement("img");\n'
           '                            img.setAttribute("src", "data:image/png;base64, " + data[item][param]);\n'
           '                            img.setAttribute("onmousemove", "zoom_in(event)");\n'
           '                            img.setAttribute("onmouseout", "zoom_out()");\n'
           '                            td.appendChild(img);\n'
           '                        } else {\n'
           '                            td.textContent = data[item][param];\n'
           '                            let copy = "navigator.clipboard.writeText(\\"" + data[item][param] + "\\")";\n'
           '                            td.setAttribute("onclick", copy);\n'
           '                        }\n'
           '                        tr.appendChild(td);\n'
           '                        i++;\n'
           '                    }\n'
           '                    tbody.appendChild(tr);\n'
           '                }\n'
           '            }\n'
           '        </script>\n'
           '    </head>\n'
           '    <body>\n'
           '        <div id="background"></div>\n'
           '        <div id="zoom"></div>\n'
           '        <div id="content">\n'
           '            <table>\n'
           '                <thead>\n'
           '                    <tr>\n'
           '                        <th colspan="5">\n'
           '                            <label>\n'
           '                                <input type="text" placeholder="Поиск" onkeyup="create_table(this.value)"/>\n'
           '                            </label>\n'
           '                        </th>\n'
           '                    </tr>\n'
           '                    <tr>\n'
           '                        <th>Номер</th>\n'
           '                        <th>Изображение</th>\n'
           '                        <th>Русское имя</th>\n'
           '                        <th>Английское имя</th>\n'
           '                        <th>ID</th>\n'
           '                    </tr>\n'
           '                </thead>\n'
           '                <tbody>\n'
           '                    <script>\n'
           '                        create_table();\n'
           '                    </script>\n'
           '                </tbody>\n'
           '            </table>\n'
           '        </div>\n'
           '    </body>\n'
           '</html>\n')

INDEX = str('<script>\n'
            '    // start data\n'
            '    let data = %s;\n'
            '    // end data\n'
            '</script>\n'
            '\n'
            '<!DOCTYPE HTML>\n'
            '<html lang="ru">\n'
            '    <head>\n'
            '        <meta charset="utf-8"/>\n'
            '        <title>Список страниц</title>\n'
            '        <meta name="description" content="Список страниц"/>\n'
            '        <meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
            '        <script>\n'
            '            (function icon() {\n'
            '                let head = document.querySelector("head");\n'
            '                let link = document.createElement("link");\n'
            '                link.setAttribute("rel", "icon");\n'
            '                link.setAttribute("href", "data:image/png;base64, " + data["1"]["img"]);\n'
            '                link.setAttribute("type", "image/png");\n'
            '                head.appendChild(link);\n'
            '            })();\n'
            '        </script>\n'
            '        <style>\n'
            '            th, td {\n'
            '                border-width: 3px;\n'
            '                border-style: solid;\n'
            '                border-color: #673ab7;\n'
            '            }\n'
            '            \n'
            '            img {\n'
            '                height: 150px;\n'
            '            }\n'
            '            \n'
            '            table {\n'
            '                margin: auto;\n'
            '            }\n'
            '            \n'
            '            #background {\n'
            '                background: #000 url("data:image/png;base64, %s") center;\n'
            '                position: fixed;\n'
            '                z-index: 1;\n'
            '                left: 0;\n'
            '                top: 0;\n'
            '                right: 0;\n'
            '                bottom: 0;\n'
            '                filter: blur(10px);\n'
            '                background-size: cover;\n'
            '            }\n'
            '            \n'
            '            #content, tbody {\n'
            '                position: relative;\n'
            '                z-index: 2;\n'
            '                text-align: center;\n'
            '                color: #000000;\n'
            '                font-size: 20px;\n'
            '                font-weight: bold;\n'
            '                text-shadow: #ffffff 3px 3px 5px, #ffffff -3px -3px 5px, #ffffff 3px -3px 5px, #ffffff -3px 3px 5px;\n'
            '            }\n'
            '            \n'
            '            #zoom {\n'
            '                display: none;\n'
            '                position: fixed;\n'
            '                z-index: 3;\n'
            '            }\n'
            '            \n'
            '            input {\n'
            '                width: 100%s;\n'
            '                height: 25px;\n'
            '                background-color: transparent;\n'
            '                color: white;\n'
            '                border: 0 transparent;\n'
            '            }\n'
            '        </style>\n'
            '        <script>\n'
            '            function zoom_in(event) {\n'
            '                let zoom = document.getElementById("zoom");\n'
            '                zoom.style.display = "block";\n'
            '                zoom.style.top = (event.y - (event["srcElement"]["naturalHeight"] / 2)).toString();\n'
            '                zoom.style.left = event.x + 50;\n'
            '                zoom.style.width = event["srcElement"]["naturalWidth"].toString();\n'
            '                zoom.style.height = event["srcElement"]["naturalHeight"].toString();\n'
            '                zoom.style.background = "url(\\"" + event["srcElement"]["currentSrc"] + "\\")";\n'
            '            }\n'
            '            \n'
            '            function zoom_out() {\n'
            '                document.getElementById("zoom").style.display = "none";\n'
            '            }\n'
            '            \n'
            '            function create_table(search) {\n'
            '                let tbody = document.querySelector("tbody");\n'
            '                tbody.innerHTML = "";\n'
            '                for (let item in data) {\n'
            '                    if (typeof search != "undefined" && search !== "") {\n'
            '                        let text = "";\n'
            '                        let i = 1;\n'
            '                        for (let param in data[item]) {\n'
            '                            if (i !== 1) {\n'
            '                                text += data[item][param]\n'
            '                            }\n'
            '                            i++;\n'
            '                        }\n'
            '                        if (!(text.toLowerCase().includes(search.toLowerCase()))) {\n'
            '                            continue;\n'
            '                        }\n'
            '                    }\n'
            '                    let tr = document.createElement("tr");\n'
            '                    let td = document.createElement("td");\n'
            '                    td.textContent = item;\n'
            '                    tr.appendChild(td);\n'
            '                    let i = 1;\n'
            '                    for (let param in data[item]) {\n'
            '                        let td = document.createElement("td");\n'
            '                        if (i === 1) {\n'
            '                            let img = document.createElement("img");\n'
            '                            img.setAttribute("src", "data:image/png;base64, " + data[item][param]);\n'
            '                            img.setAttribute("onmousemove", "zoom_in(event)");\n'
            '                            img.setAttribute("onmouseout", "zoom_out()");\n'
            '                            td.appendChild(img);\n'
            '                        } else if (i === 2) {\n'
            '                            let a = document.createElement("a");\n'
            '                            a.setAttribute("href", data[item][param]);\n'
            '                            a.textContent = data[item][param];\n'
            '                            td.appendChild(a);\n'
            '                        } else {\n'
            '                            td.textContent = data[item][param];\n'
            '                           let copy = "navigator.clipboard.writeText(\\"" + data[item][param] + "\\")";'
            '                            td.setAttribute("onclick", copy);\n'
            '                        }\n'
            '                        tr.appendChild(td);\n'
            '                        i++;\n'
            '                    }\n'
            '                    tbody.appendChild(tr);\n'
            '                }\n'
            '            }\n'
            '        </script>\n'
            '    </head>\n'
            '    <body>\n'
            '        <div id="background"></div>\n'
            '        <div id="zoom"></div>\n'
            '        <div id="content">\n'
            '            <table>\n'
            '                <thead>\n'
            '                    <tr>\n'
            '                        <th colspan="5">\n'
            '                            <label>\n'
            '                                <input type="text" placeholder="Поиск" onkeyup="create_table(this.value)"/>\n'
            '                            </label>\n'
            '                        </th>\n'
            '                    </tr>\n'
            '                    <tr>\n'
            '                        <th>Номер</th>\n'
            '                        <th>Изображение</th>\n'
            '                        <th>Страница</th>\n'
            '                        <th>Описание</th>\n'
            '                        <th>Размер страницы</th>\n'
            '                    </tr>\n'
            '                </thead>\n'
            '                <tbody>\n'
            '                    <script>\n'
            '                        create_table();\n'
            '                    </script>\n'
            '                </tbody>\n'
            '            </table>\n'
            '        </div>\n'
            '    </body>\n'
            '</html>\n')

SETTINGS = {"Consumable": False,
            "Decore": False,
            "DestroyedHouse": False,
            "EquestriaGirls": False,
            "ExpansionZone": False,
            "Inn": False,
            "MasterExpansionZone": False,
            "PartySceneDecore": False,
            "Path": False,
            "Pony": False,
            "Pony_House": False,
            "PonyPart": False,
            "PonySet": False,
            "ProfileAvatar": False,
            "ProfileAvatarFrame": False,
            "ProgressBooster": False,
            "QuestSpecialItem": False,
            "TapableContainer": False,
            "Theme": False,
            "Totem": False,
            "TravelersCafe": False}

CATEGORIES = {"Consumable": [["Name", "Unlocal"], ["Graphic", "Sprite"], FAKE_ALL],
              "Decore": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_DECORE],
              "DestroyedHouse": [["Name", "Unlocal"], ["Icon", "QuestIcon"], FAKE_HOUSE],
              "EquestriaGirls": [["Name", "Unlocal"], ["Icons", "Icons_Avatar"], FAKE_ALL],
              "ExpansionZone": [["ExpansionPopup", "Description"], ["ExpansionPopup", "Image"], FAKE_ALL],
              "Inn": [["Name", "Unlocal"], ["Icon", "BookIcon"], FAKE_ALL],
              "MasterExpansionZone": [["Unlock", "UnavailableText"], ["Unlock", "UnavailableImage"], FAKE_ALL],
              "PartySceneDecore": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_DECORE],
              "Path": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_ALL],
              "Pony": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_PONY],
              "Pony_House": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_HOUSE],
              "PonyPart": [["PonyPart", "ModelName"], ["PonyPart", "Icon"], FAKE_ALL],
              "PonySet": [["PonySet", "Localization"], ["PonySet", "Icon"], FAKE_ALL],
              "ProfileAvatar": [["Shop", "Label"], ["Settings", "PictureActive"], FAKE_ALL],
              "ProfileAvatarFrame": [["Shop", "Label"], ["Shop", "Icon"], FAKE_ALL],
              "ProgressBooster": [["Shop", "Label"], ["Shop", "Icon"], FAKE_ALL],
              "QuestSpecialItem": [["QuestSpecialItem", "Name"], ["QuestSpecialItem", "Icon"], FAKE_ALL],
              "TapableContainer": [["UI", "TaskName"], ["UI", "Icon"], FAKE_ALL],
              "Theme": [["Appearance", "Name"], ["Appearance", "Image"], FAKE_ALL],
              "Totem": [["Name", "Unlocal"], ["Production", "ShopIcon"], FAKE_ALL],
              "TravelersCafe": [["Name", "Unlocal"], ["Shop", "Icon"], FAKE_HOUSE]}

DESCRIPTION = {"Consumable": "Расходный материал",
               "Decore": "Декор",
               "DestroyedHouse": "Разрушенные дома",
               "EquestriaGirls": "Девочки из Эквестрии",
               "ExpansionZone": "",
               "Inn": "",
               "MasterExpansionZone": "",
               "PartySceneDecore": "Праздничная сцена",
               "Path": "Дорожки",
               "Pony": "Персонажи",
               "Pony_House": "Магазины и дома",
               "PonyPart": "Костюмы",
               "PonySet": "Наборы костюмов",
               "ProfileAvatar": "Аватары",
               "ProfileAvatarFrame": "Рамки аватаров",
               "ProgressBooster": "Бустеры",
               "QuestSpecialItem": "Предметы квестов",
               "TapableContainer": "",
               "Theme": "Темы",
               "Totem": "Тотемы",
               "TravelersCafe": "Отель \"Золотая подкова\""}

FOLDERS = [["000_and_mlpextra_common"],
           ["000_and_mlpextra_pvr_common", "000_and_mlpextra_astc_pvr_common"],
           ["000_and_mlpextra_veryhigh", "000_and_mlpextra_astc_veryhigh"],
           ["000_and_mlpextra2_pvr_common", "000_and_mlpextra2_astc_pvr_common"],
           ["000_and_mlpextra2_veryhigh", "000_and_mlpextra2_astc_veryhigh"],
           ["000_and_mlpextragui_veryhigh/gui", "000_and_mlpextragui_astc_veryhigh/gui"],
           ["000_and_startup_common"],
           ["001_and_mlpdata_veryhigh", "001_and_mlpdata_astc_veryhigh"]]


def create_file_settings(data=None):
    try:
        print("0: Создание файла TABLEcreator.json.\n")
        with open(file="TABLEcreator.json",
                  mode="w") as settings_json:
            dump(obj=data or SETTINGS,
                 fp=settings_json,
                 indent=4)
        return data or SETTINGS
    except Exception:
        print("[ERROR] Во время создания файла настроек TABLEcreator.json возникла ошибка. "
              "Возможно нет прав на создания файлов.\n")
        return data or SETTINGS


def create_file_html(data):
    try:
        splash, trigger, index_html, i = "", True, {}, 1
        try:
            with open(file="000_and_startup_common/mlp_splash.png",
                      mode="rb") as mlp_splash_png:
                splash = b64encode(s=mlp_splash_png.read()).decode(encoding="UTF-8",
                                                                   errors="ignore")
        except Exception:
            print("[ERROR] Во время обработки файла 000_and_startup_common/mlp_splash.png возникла ошибка. "
                  "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
            trigger = False
        if not exists(path="HTML"):
            print(f"6: Создание папки HTML.\n")
            try:
                makedirs(name="HTML")
            except Exception:
                print(f"[ERROR] Во время создания папки HTML возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")
                trigger = False
        for cat in data:
            print(f"6: Создание файла HTML/{cat}.html.\n")
            try:
                html = HTML % (dumps(obj=data[cat],
                                     indent=4,
                                     ensure_ascii=False), cat, cat, splash, "%")
                with open(file=f"HTML/{cat}.html",
                          mode="w",
                          encoding="UTF-8") as output_html:
                    output_html.write(html)
                index_html.update({i: {"img": data[cat][1]["img"],
                                       "page": f"{cat}.html",
                                       "desc": DESCRIPTION[cat],
                                       "size": f"{str(len(html) / 1024 / 1024)[:4]} МБ"}})
                i += 1
            except Exception:
                print(f"[WARNING] Во время создания файла HTML/{cat}.html возникла ошибка. "
                      f"Возможно нет прав на создания файлов. "
                      f"Файл пропущен.\n")
                trigger = False
        try:
            print("7: Создание файла HTML/index.html.\n")
            with open(file="HTML/index.html",
                      mode="w",
                      encoding="UTF-8") as output_index_html:
                output_index_html.write(INDEX % (dumps(obj=index_html,
                                                       indent=4,
                                                       ensure_ascii=False), splash, "%"))
        except Exception:
            print("[WARNING] Во время создания файла HTML/index.html возникла ошибка. "
                  "Возможно нет прав на создания файлов. "
                  "Файл пропущен.\n")
            trigger = False
        return trigger
    except Exception:
        print(f"[ERROR] Во время создания HTML файлов возникла ошибка. "
              f"Возможно нет прав на создания файлов.\n")
        return False


def load_file_settings():
    try:
        if exists(path="TABLEcreator.json"):
            print("1: Обработка файла TABLEcreator.json.\n")
            with open(file="TABLEcreator.json",
                      mode="r",
                      encoding="UTF-8") as settings_json:
                try:
                    data = loads(s=settings_json.read())
                    if len(data) < len(SETTINGS):
                        print("[INFO] В файле настроек TABLEcreator.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")
                        for item in SETTINGS:
                            if item not in data:
                                data.update({item: SETTINGS[item]})
                        return create_file_settings(data=data)
                    else:
                        return data
                except Exception:
                    print("[INFO] Не удалось прочитать файл настроек TABLEcreator.json. "
                          "Возможно данные в файле повреждены. "
                          "Будет создан новый файл со стандартными настройками.\n")
                    return create_file_settings()
        else:
            print("[INFO] Файл настроек TABLEcreator.json не обнаружен. "
                  "Будет создан новый файл со стандартными настройками.\n")
            return create_file_settings()
    except Exception:
        print("[ERROR] Во время обработки файла настроек TABLEcreator.json возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        return SETTINGS


def load_russian_strings():
    try:
        russian_list = {}
        if exists(path="000_and_startup_common/russian.txt"):
            print("2: Обработка файла 000_and_startup_common/russian.txt.\n")
            with open(file="000_and_startup_common/russian.txt",
                      mode="r",
                      encoding="UTF-8") as russian_file:
                for line in russian_file.readlines():
                    data = line.split("=")
                    if len(data) == 2 and data[0] != "":
                        russian_list.update({data[0].strip(): data[1].strip()})
                return russian_list
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла russian.txt. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")
            return None
    except Exception:
        print("[ERROR] Во время обработки файла 000_and_startup_common/russian.txt возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        return None


def load_english_strings():
    try:
        english_list = {}
        if exists(path="000_and_startup_common/english.txt"):
            print("3: Обработка файла 000_and_startup_common/english.txt.\n")
            with open(file="000_and_startup_common/english.txt",
                      mode="r",
                      encoding="UTF-8") as english_file:
                for line in english_file.readlines():
                    data = line.split("=")
                    if len(data) == 2 and data[0] != "":
                        english_list.update({data[0].strip(): data[1].strip()})
                return english_list
        else:
            print("[ERROR] Отсутствует папка 000_and_startup_common или в ней нет файла english.txt. "
                  "Разархивируйте архив 000_and_startup_common.ark используя программу ARKdumper. "
                  "В настройках программы ARKdumper обязательно установите Convert = 1.\n")
            return None
    except Exception:
        print("[ERROR] Во время обработки файла 000_and_startup_common/english.txt возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        return None


def load_image_folders():
    try:
        image_list, trigger = {}, True
        for folder in FOLDERS:
            if exists(path=folder[0]):
                print(f"4: Обработка папки {folder[0]}.\n")
                try:
                    for root, dirs, files in walk(top=folder[0]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\", "/")
                                image_list.update({file: f"{folder}/{file}"})
                except Exception:
                    print(f"[ERROR] Во время обработки файлов в папке {folder[0]} возникла ошибка. "
                          f"Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")
                    trigger = False
            elif len(folder) == 2 and exists(path=folder[1]):
                print(f"4: Обработка папки {folder[1]}.\n")
                try:
                    for root, dirs, files in walk(top=folder[1]):
                        for file in files:
                            if file.endswith(".png"):
                                folder = root.replace("\\", "/")
                                image_list.update({file: f"{folder}/{file}"})
                except Exception:
                    print(f"[ERROR] Во время обработки файлов в папке {folder[1]} возникла ошибка. "
                          f"Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")
                    trigger = False
            else:
                if len(folder) == 1:
                    print(f"[ERROR] Отсутствует папка {folder[0]} или в ней нет файлов. "
                          f"Разархивируйте архив {folder[0]}.ark используя программу ARKdumper. "
                          f"В настройках программы ARKdumper обязательно установите Convert = 1 и Split = 1.\n")
                else:
                    print(f"[ERROR] Отсутствуют папки {folder[0]} и {folder[1]} или в них нет файлов. "
                          f"Для работы программы нужна хотябы одна их них. "
                          f"Разархивируйте архив {folder[0]}.ark или {folder[1]}.ark используя программу ARKdumper. "
                          f"В настройках программы ARKdumper обязательно установите Convert = 1 и Split = 1.\n")
                trigger = False
        if trigger:
            return image_list
        else:
            return None
    except Exception:
        folders = ", ".join([", ".join(x) if len(x) == 2 else x[0] for x in FOLDERS])
        print(f"[ERROR] Во время обработки PNG файлов в папках {folders} возникла ошибка. "
              f"Возможно файлы в папках повреждены или нет прав на чтение файлов.\n")
        return None


def parse_gameobjectdata(settings, russian, english, images):
    try:
        all_data, trigger = {}, True
        if not exists(path="000_and_mlpextra_common/gameobjectdata.xml"):
            print("[ERROR] Отсутствует папка 000_and_mlpextra_common или в ней нет файла gameobjectdata.xml. "
                  "Разархивируйте архив 000_and_mlpextra_common.ark используя программу ARKdumper.\n")
            trigger = False
        if True not in settings.values():
            print("[ERROR] В файле настроек TABLEcreator.json не включен ни один параметр. "
                  "Для работы программы нужно включить хотя бы один.\n")
            trigger = False
        if trigger and russian is not None and english is not None and images is not None:
            print("5: Обработка файла 000_and_mlpextra_common/gameobjectdata.xml.")
            with open(file="000_and_mlpextra_common/gameobjectdata.xml",
                      mode="r",
                      encoding="UTF-8") as gameobjectdata_xml:
                soup = BeautifulSoup(markup=gameobjectdata_xml.read(),
                                     features="xml").find_all(name="GameObjects",
                                                              limit=1)[0]
                for cat in settings:
                    if settings[cat] and cat in CATEGORIES:
                        print(f"    Поиск всех {cat}...")
                        try:
                            data, i = {}, 1
                            for item in soup.find_all(name="Category",
                                                      attrs={"ID": cat},
                                                      limit=1)[0]:
                                if len(item) > 1:
                                    res_id, res_rus, res_eng, res_img = "", "", "", CATEGORIES[cat][2]
                                    try:
                                        res_id = item["ID"]
                                    except Exception:
                                        pass
                                    try:
                                        res_rus = russian[item.find_all(name=CATEGORIES[cat][0][0],
                                                                        limit=1)[0][CATEGORIES[cat][0][1]]]
                                    except Exception:
                                        pass
                                    try:
                                        res_eng = english[item.find_all(name=CATEGORIES[cat][0][0],
                                                                        limit=1)[0][CATEGORIES[cat][0][1]]]
                                    except Exception:
                                        pass
                                    try:
                                        image = item.find_all(name=CATEGORIES[cat][1][0],
                                                              limit=1)[0][CATEGORIES[cat][1][1]].replace("gui/", "")
                                        with open(file=images[image],
                                                  mode="rb") as image_file:
                                            res_img = b64encode(s=image_file.read()).decode(encoding="UTF-8",
                                                                                            errors="ignore")
                                    except Exception:
                                        pass
                                    if res_rus != "" or res_eng != "" or res_img != CATEGORIES[cat][2]:
                                        data.update({i: {"img": res_img,
                                                         "rus": res_rus,
                                                         "eng": res_eng,
                                                         "id": res_id}})
                                        i += 1
                            all_data.update({cat: data})
                        except Exception:
                            print("")
                            print(f"[WARNING] Во время обработки категории {cat} возникла ошибка. "
                                  f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                                  f"Категория пропущена.\n")
                            trigger = False
                if len(all_data) > 0:
                    print("")
                    trigger = create_file_html(data=all_data) if trigger else False
                return trigger
        else:
            return False
    except Exception:
        print("")
        print("[ERROR] Во время обработки файла 000_and_mlpextra_common/gameobjectdata.xml возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        return False


if __name__ == "__main__":
    try:
        if parse_gameobjectdata(settings=load_file_settings(),
                                russian=load_russian_strings(),
                                english=load_english_strings(),
                                images=load_image_folders()):
            exit()
        else:
            raise Exception
    except Exception:
        input()
        exit()
