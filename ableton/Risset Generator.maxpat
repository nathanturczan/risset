{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 6,
			"revision" : 0,
			"architecture" : "x64",
			"modernui" : 1
		},
		"classnamespace" : "box",
		"rect" : [ 100.0, 100.0, 600.0, 500.0 ],
		"bglocked" : 0,
		"openinpresentation" : 1,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "Risset Rhythm Generator - Polyrhythmic MIDI Tool",
		"digest" : "Generate polyrhythmic Risset rhythm patterns",
		"tags" : "MIDI Tool, Generator, Risset, Polyrhythm",
		"style" : "",
		"subpatcher_template" : "",
		"assistshowspatchername" : 0,
		"boxes" : [
			{
				"box" : 				{
					"id" : "obj-jweb",
					"maxclass" : "jweb",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 200.0, 50.0, 340.0, 220.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 0.0, 0.0, 340.0, 220.0 ],
					"rendermode" : 0,
					"url" : "risset-ui.html"
				}
			},
			{
				"box" : 				{
					"id" : "obj-route",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 6,
					"outlettype" : [ "", "", "", "", "", "" ],
					"patching_rect" : [ 200.0, 290.0, 320.0, 22.0 ],
					"text" : "route direction mode ratio pitchHigh pitchLow"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-dir",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 200.0, 330.0, 95.0, 22.0 ],
					"text" : "prepend setDirection"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-mode",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 270.0, 330.0, 85.0, 22.0 ],
					"text" : "prepend setMode"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-ratio",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 340.0, 330.0, 85.0, 22.0 ],
					"text" : "prepend setRatio"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-phigh",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 410.0, 330.0, 100.0, 22.0 ],
					"text" : "prepend setPitchHigh"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-plow",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 480.0, 330.0, 100.0, 22.0 ],
					"text" : "prepend setPitchLow"
				}
			},
			{
				"box" : 				{
					"id" : "obj-miditool-in",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 50.0, 50.0, 100.0, 22.0 ],
					"text" : "live.miditool.in"
				}
			},
			{
				"box" : 				{
					"id" : "obj-js",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 390.0, 140.0, 22.0 ],
					"text" : "js @immediate 1 risset.js"
				}
			},
			{
				"box" : 				{
					"id" : "obj-miditool-out",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 430.0, 105.0, 22.0 ],
					"text" : "live.miditool.out"
				}
			},
			{
				"box" : 				{
					"id" : "obj-comment",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 20.0, 300.0, 20.0 ],
					"text" : "Risset Rhythm Generator - Polyrhythmic MIDI Tool"
				}
			}
		],
		"lines" : [
			{
				"patchline" : 				{
					"destination" : [ "obj-route", 0 ],
					"source" : [ "obj-jweb", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-dir", 0 ],
					"source" : [ "obj-route", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-mode", 0 ],
					"source" : [ "obj-route", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-ratio", 0 ],
					"source" : [ "obj-route", 2 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-phigh", 0 ],
					"source" : [ "obj-route", 3 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-plow", 0 ],
					"source" : [ "obj-route", 4 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-dir", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-mode", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-ratio", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-phigh", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-plow", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-miditool-in", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-miditool-out", 0 ],
					"source" : [ "obj-js", 0 ]
				}
			}
		],
		"dependency_cache" : [
			{
				"name" : "risset.js",
				"bootpath" : "~/Github/risset/Ableton",
				"type" : "TEXT",
				"implicit" : 1
			},
			{
				"name" : "risset-ui.html",
				"bootpath" : "~/Github/risset/Ableton",
				"type" : "TEXT",
				"implicit" : 1
			}
		],
		"autosave" : 0
	}
}
