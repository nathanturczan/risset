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
		"rect" : [ 100.0, 100.0, 800.0, 600.0 ],
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
		"boxes" : [ 			{
				"box" : 				{
					"id" : "obj-1",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 50.0, 50.0, 120.0, 22.0 ],
					"text" : "live.miditool.in"
				}
			},
			{
				"box" : 				{
					"id" : "obj-2",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 300.0, 120.0, 22.0 ],
					"text" : "live.miditool.out"
				}
			},
			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 150.0, 80.0, 22.0 ],
					"text" : "js risset.js"
				}
			},
			{
				"box" : 				{
					"id" : "obj-4",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "" ],
					"patching_rect" : [ 50.0, 100.0, 60.0, 22.0 ],
					"text" : "t b b"
				}
			},
			{
				"box" : 				{
					"id" : "obj-5",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 200.0, 100.0, 22.0 ],
					"text" : "fromsymbol"
				}
			},
			{
				"box" : 				{
					"id" : "obj-6",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 250.0, 100.0, 22.0 ],
					"text" : "dict.deserialize"
				}
			},
			{
				"box" : 				{
					"id" : "obj-10",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 200.0, 80.0, 44.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 10.0, 44.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 2 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Ratio Num",
							"parameter_mmax" : 9.0,
							"parameter_mmin" : 1.0,
							"parameter_shortname" : "Num",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0
						}
					},
					"varname" : "ratio_num"
				}
			},
			{
				"box" : 				{
					"id" : "obj-11",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 260.0, 80.0, 44.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 60.0, 10.0, 44.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 1 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Ratio Den",
							"parameter_mmax" : 9.0,
							"parameter_mmin" : 1.0,
							"parameter_shortname" : "Den",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0
						}
					},
					"varname" : "ratio_den"
				}
			},
			{
				"box" : 				{
					"id" : "obj-12",
					"maxclass" : "live.menu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 320.0, 80.0, 70.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 110.0, 25.0, 70.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_enum" : [ "Accel", "Decel" ],
							"parameter_initial" : [ 0 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Direction",
							"parameter_mmax" : 1,
							"parameter_shortname" : "Dir",
							"parameter_type" : 2
						}
					},
					"varname" : "direction"
				}
			},
			{
				"box" : 				{
					"id" : "obj-13",
					"maxclass" : "live.menu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 400.0, 80.0, 60.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 110.0, 45.0, 60.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_enum" : [ "Arc", "Ramp" ],
							"parameter_initial" : [ 0 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Mode",
							"parameter_mmax" : 1,
							"parameter_shortname" : "Mode",
							"parameter_type" : 2
						}
					},
					"varname" : "mode"
				}
			},
			{
				"box" : 				{
					"id" : "obj-14",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 480.0, 80.0, 44.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 185.0, 10.0, 44.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 4 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Measures",
							"parameter_mmax" : 16.0,
							"parameter_mmin" : 1.0,
							"parameter_shortname" : "Meas",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0
						}
					},
					"varname" : "measures"
				}
			},
			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 540.0, 80.0, 44.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 235.0, 10.0, 44.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 60 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Pitch Low",
							"parameter_mmax" : 127.0,
							"parameter_mmin" : 0.0,
							"parameter_shortname" : "Low",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0
						}
					},
					"varname" : "pitch_low"
				}
			},
			{
				"box" : 				{
					"id" : "obj-16",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 600.0, 80.0, 44.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 285.0, 10.0, 44.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 64 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Pitch High",
							"parameter_mmax" : 127.0,
							"parameter_mmin" : 0.0,
							"parameter_shortname" : "High",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0
						}
					},
					"varname" : "pitch_high"
				}
			},
			{
				"box" : 				{
					"id" : "obj-20",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 200.0, 140.0, 80.0, 22.0 ],
					"text" : "pack i i"
				}
			},
			{
				"box" : 				{
					"id" : "obj-21",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 200.0, 170.0, 90.0, 22.0 ],
					"text" : "prepend setRatio"
				}
			},
			{
				"box" : 				{
					"id" : "obj-22",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 320.0, 140.0, 110.0, 22.0 ],
					"text" : "prepend setDirection"
				}
			},
			{
				"box" : 				{
					"id" : "obj-23",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 400.0, 140.0, 95.0, 22.0 ],
					"text" : "prepend setMode"
				}
			},
			{
				"box" : 				{
					"id" : "obj-24",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 480.0, 140.0, 110.0, 22.0 ],
					"text" : "prepend setMeasures"
				}
			},
			{
				"box" : 				{
					"id" : "obj-25",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 540.0, 140.0, 105.0, 22.0 ],
					"text" : "prepend setPitchLow"
				}
			},
			{
				"box" : 				{
					"id" : "obj-26",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 600.0, 140.0, 110.0, 22.0 ],
					"text" : "prepend setPitchHigh"
				}
			},
			{
				"box" : 				{
					"id" : "obj-30",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 20.0, 300.0, 20.0 ],
					"text" : "Risset Rhythm Generator - Polyrhythmic MIDI Tool"
				}
			}
		],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-1", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-20", 0 ],
					"source" : [ "obj-10", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-20", 1 ],
					"source" : [ "obj-11", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-22", 0 ],
					"source" : [ "obj-12", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-23", 0 ],
					"source" : [ "obj-13", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-24", 0 ],
					"source" : [ "obj-14", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-25", 0 ],
					"source" : [ "obj-15", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-26", 0 ],
					"source" : [ "obj-16", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-21", 0 ],
					"source" : [ "obj-20", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-21", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-22", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-23", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-24", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-25", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-26", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"source" : [ "obj-3", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-4", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-6", 0 ],
					"source" : [ "obj-5", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-6", 0 ]
				}
			}
		],
		"parameters" : 		{
			"obj-10" : [ "Ratio Num", "Num", 0 ],
			"obj-11" : [ "Ratio Den", "Den", 0 ],
			"obj-12" : [ "Direction", "Dir", 0 ],
			"obj-13" : [ "Mode", "Mode", 0 ],
			"obj-14" : [ "Measures", "Meas", 0 ],
			"obj-15" : [ "Pitch Low", "Low", 0 ],
			"obj-16" : [ "Pitch High", "High", 0 ],
			"parameterbanks" : 			{

			},
			"inherited_shortname" : 1
		},
		"dependency_cache" : [ 			{
				"name" : "risset.js",
				"bootpath" : "~/Github/risset/ableton",
				"type" : "TEXT",
				"implicit" : 1
			}
		],
		"autosave" : 0
	}
}
