Nagamochi
====

Nagamochi is a library of Digital Assets, Presets, Shelves and Scripts for SideFX Houdini.

### Features

- otls
- Shelf 
- Right-click on parm menu
- Pressets


### Requirement

Houdini 18.0 or Higher

### Installation
1. Save this repository wherever you like.
2. Copy the Nagamochi.json file from the location used in step 1 to $HOME/Houdini19.5/packages, and change the contained paths to match the location chosen in step 1.

```json
{
    "env" : 
    [
        {   "NAGAMOCHI" : "PLACE_TO_INSTALL"  },

        {   "HOUDINI_PATH" :
        	{
        		"value":
        			[        				
                        "$NAGAMOCHI/common",
        				"$NAGAMOCHI/houdini$HOUDINI_MAJOR_RELEASE.$HOUDINI_MINOR_RELEASE",                       
        			],
        	}
        },
        
        {   "NM_CACHE_HOU" : "HIP_VAR/../caches"  },
    ]
}
```

### Tutorials 
https://vimeo.com/shohey
[OTL]
- SOP
	- nmCameraClipPoints https://vimeo.com/388993350
- DOP
	- nmGasAge https://vimeo.com/386939150

### Future Work
- Python 3
- Create a video that how to use tools
- Clean up some scripts
- Support Windows users. (I'm developing this tool on Linux(mint/CentOS).)

### Author

* Shohei Okazaki

### Note
Nagamochi has two meanings, 「長持」 and 「長持ち」.
長持 is the toolbox of old Japanese folklore.
And 長持ち means 'long-lasting'.

Nagamochi aims to be the toolbox that does not bound by Houdini version.
