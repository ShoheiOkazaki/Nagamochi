Nagamochi
====

Nagamochi is a library of Digital Assets, Presets, Shelves, and Scripts for SideFX Houdini.

### Features

- otls
- Shelf 
- Right-click on parm menu
- Presets


### Requirement

Houdini 18.5 or Higher

### Installation
1. Save this repository wherever you want.
2. Copy the Nagamochi.json file from the location you used in step 1 to $HOME/Houdini19.5/packages and change the contained paths to match the location you chose in step 1.

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

        {   "NM_RV_PATH" : "C:/Program Files/ShotGrid/RV-2023.0.0/bin/rv.exe"  },
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
- Create a video about how to use tools
- Clean up some scripts

### Author

* Shohei Okazaki

### Note
Nagamochi has two meanings, 「長持」 and 「長持ち」.
長持 is the toolbox of old Japanese folklore.
And 長持ち means 'long-lasting'.

Nagamochi aims to be the toolbox separate from the Houdini version.

I'm making it under Windows 10 and Mint 21.
