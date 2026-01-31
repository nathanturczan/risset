{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 9,
			"minor" : 0,
			"revision" : 10,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 218.0, 149.0, 963.0, 704.0 ],
		"openinpresentation" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"description" : "Risset Rhythm Generator - Polyrhythmic MIDI Tool",
		"digest" : "Generate polyrhythmic Risset rhythm patterns",
		"tags" : "MIDI Tool, Generator, Risset, Polyrhythm",
		"boxes" : [ 			{
				"box" : 				{
					"disablefind" : 0,
					"id" : "obj-jweb",
					"maxclass" : "jweb",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 400.0, 50.0, 340.0, 220.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 0.0, 0.0, 340.0, 220.0 ],
					"rendermode" : 0,
					"url" : "file://risset-ui.html"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-route",
					"maxclass" : "newobj",
					"numinlets" : 6,
					"numoutlets" : 6,
					"outlettype" : [ "", "", "", "", "", "" ],
					"patching_rect" : [ 400.0, 290.0, 320.0, 22.0 ],
					"text" : "route direction mode ratio pitchHigh pitchLow"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-prepend-dir",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 400.0, 330.0, 119.0, 22.0 ],
					"text" : "prepend setDirection"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-prepend-mode",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 470.0, 330.0, 102.0, 22.0 ],
					"text" : "prepend setMode"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-prepend-ratio",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 540.0, 330.0, 100.0, 22.0 ],
					"text" : "prepend setRatio"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-prepend-phigh",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 610.0, 330.0, 123.0, 22.0 ],
					"text" : "prepend setPitchHigh"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-prepend-plow",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 680.0, 330.0, 121.0, 22.0 ],
					"text" : "prepend setPitchLow"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-miditool-in",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 50.0, 50.0, 100.0, 22.0 ],
					"text" : "live.miditool.in"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-js",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 150.0, 80.0, 22.0 ],
					"saved_object_attributes" : 					{
						"filename" : "risset.js",
						"parameter_enable" : 0
					}
,
					"text" : "js risset.js"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-fromsymbol",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 200.0, 75.0, 22.0 ],
					"text" : "fromsymbol"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-deserialize",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "dictionary" ],
					"patching_rect" : [ 50.0, 250.0, 90.0, 22.0 ],
					"text" : "dict.deserialize"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-miditool-out",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 300.0, 105.0, 22.0 ],
					"text" : "live.miditool.out"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-comment",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 20.0, 300.0, 20.0 ],
					"text" : "Polymetric Risset Rhythm MIDI Generator Tool"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-miditool-out", 0 ],
					"source" : [ "obj-deserialize", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-deserialize", 0 ],
					"source" : [ "obj-fromsymbol", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-fromsymbol", 0 ],
					"source" : [ "obj-js", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-route", 0 ],
					"source" : [ "obj-jweb", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-miditool-in", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-dir", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-mode", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-phigh", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-plow", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-ratio", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-dir", 0 ],
					"source" : [ "obj-route", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-mode", 0 ],
					"source" : [ "obj-route", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-phigh", 0 ],
					"source" : [ "obj-route", 3 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-plow", 0 ],
					"source" : [ "obj-route", 4 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-ratio", 0 ],
					"source" : [ "obj-route", 2 ]
				}

			}
 ],
		"dependency_cache" : [ 			{
				"name" : "risset.js",
				"bootpath" : "~/Github/risset/ableton",
				"patcherrelativepath" : ".",
				"type" : "TEXT",
				"implicit" : 1
			}
 ],
		"autosave" : 0
	}

}
