{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 9,
			"minor" : 0,
			"revision" : 10,
			"architecture" : "x64",
			"modernui" : 1
		},
		"classnamespace" : "box",
		"rect" : [ 100.0, 100.0, 800.0, 600.0 ],
		"openinpresentation" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"description" : "Risset Rhythm Generator - Native UI",
		"digest" : "Generate polyrhythmic Risset rhythm patterns",
		"tags" : "MIDI Tool, Generator, Risset, Polyrhythm",
		"boxes" : [
			{
				"box" : 				{
					"id" : "obj-direction-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 20.0, 70.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 5.0, 70.0, 18.0 ],
					"text" : "DIRECTION",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-direction",
					"maxclass" : "live.tab",
					"numinlets" : 1,
					"numoutlets" : 3,
					"num_lines_patching" : 1,
					"num_lines_presentation" : 1,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 40.0, 100.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 22.0, 100.0, 20.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_enum" : [ "Accel", "Decel" ],
							"parameter_initial" : [ 0 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Direction",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Direction",
							"parameter_type" : 2,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "Sets whether the rhythm accelerates or decelerates over time.",
							"parameter_annotation_name" : "Risset: Direction"
						}
					},
					"varname" : "Direction"
				}
			},
			{
				"box" : 				{
					"id" : "obj-mode-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 140.0, 20.0, 50.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 120.0, 5.0, 50.0, 18.0 ],
					"text" : "MODE",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-mode",
					"maxclass" : "live.menu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 140.0, 40.0, 70.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 120.0, 22.0, 70.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_enum" : [ "Arc", "Ramp" ],
							"parameter_initial" : [ 0 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Mode",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Mode",
							"parameter_type" : 2,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "Arc outputs 2 metabars (complete cycle). Ramp outputs 1 metabar (building block).",
							"parameter_annotation_name" : "Risset: Mode"
						}
					},
					"varname" : "Mode"
				}
			},
			{
				"box" : 				{
					"id" : "obj-ratio-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 80.0, 50.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 50.0, 50.0, 18.0 ],
					"text" : "RATIO",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-ratio-num",
					"maxclass" : "live.numbox",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 100.0, 44.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 68.0, 44.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 2 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Ratio Numerator",
							"parameter_mmax" : 9.0,
							"parameter_mmin" : 1.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Num",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "The numerator of the tempo ratio. For acceleration, this should be smaller than the denominator.",
							"parameter_annotation_name" : "Risset: Ratio Numerator"
						}
					},
					"varname" : "RatioNum"
				}
			},
			{
				"box" : 				{
					"id" : "obj-ratio-den",
					"maxclass" : "live.numbox",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 120.0, 44.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 85.0, 44.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 3 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Ratio Denominator",
							"parameter_mmax" : 9.0,
							"parameter_mmin" : 1.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Den",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "The denominator of the tempo ratio. For acceleration, this should be larger than the numerator.",
							"parameter_annotation_name" : "Risset: Ratio Denominator"
						}
					},
					"varname" : "RatioDen"
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-high-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 80.0, 80.0, 60.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 70.0, 50.0, 60.0, 18.0 ],
					"text" : "HIGH (IN)",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-high",
					"maxclass" : "live.numbox",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 80.0, 100.0, 44.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 70.0, 68.0, 44.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 64 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "High Pitch",
							"parameter_mmax" : 127.0,
							"parameter_mmin" : 0.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "High",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "MIDI pitch for the layer that fades in (gets louder).",
							"parameter_annotation_name" : "Risset: High Pitch"
						}
					},
					"varname" : "PitchHigh"
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-low-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 150.0, 80.0, 60.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 140.0, 50.0, 65.0, 18.0 ],
					"text" : "LOW (OUT)",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-low",
					"maxclass" : "live.numbox",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 150.0, 100.0, 44.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 140.0, 68.0, 44.0, 15.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 60 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Low Pitch",
							"parameter_mmax" : 127.0,
							"parameter_mmin" : 0.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Low",
							"parameter_type" : 1,
							"parameter_unitstyle" : 0,
							"parameter_annotation" : "MIDI pitch for the layer that fades out (gets quieter).",
							"parameter_annotation_name" : "Risset: Low Pitch"
						}
					},
					"varname" : "PitchLow"
				}
			},
			{
				"box" : 				{
					"id" : "obj-velocity-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 150.0, 120.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 108.0, 120.0, 18.0 ],
					"text" : "VELOCITY RESPONSE",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-velocity",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 170.0, 41.0, 48.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 125.0, 41.0, 48.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_initial" : [ 1.5 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "Velocity Response",
							"parameter_mmax" : 3.0,
							"parameter_mmin" : 0.5,
							"parameter_modmode" : 0,
							"parameter_shortname" : "Vel",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1,
							"parameter_annotation" : "Shapes the velocity crossfade curve. Lower values (0.5) are punchier, higher values (3.0) are gentler.",
							"parameter_annotation_name" : "Risset: Velocity Response"
						}
					},
					"varname" : "VelocityResponse"
				}
			},
			{
				"box" : 				{
					"id" : "obj-constraint",
					"maxclass" : "live.text",
					"numinlets" : 1,
					"numoutlets" : 2,
					"mode" : 0,
					"outlettype" : [ "", "" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 230.0, 180.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 10.0, 180.0, 195.0, 20.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_longname" : "Constraint",
							"parameter_modmode" : 0,
							"parameter_shortname" : "Constraint",
							"parameter_type" : 2,
							"parameter_annotation" : "Shows the current ratio and direction constraint. Accel requires Num < Den, Decel requires Num > Den.",
							"parameter_annotation_name" : "Risset: Constraint"
						}
					},
					"text" : "2/3 Num < Denom → accel",
					"varname" : "Constraint"
				}
			},
			{
				"box" : 				{
					"id" : "obj-miditool-in",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 300.0, 50.0, 100.0, 22.0 ],
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
					"patching_rect" : [ 300.0, 150.0, 80.0, 22.0 ],
					"saved_object_attributes" : 					{
						"filename" : "risset.js",
						"parameter_enable" : 0
					},
					"text" : "js risset.js"
				}
			},
			{
				"box" : 				{
					"id" : "obj-miditool-out",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 300.0, 200.0, 105.0, 22.0 ],
					"text" : "live.miditool.out"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-dir",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 80.0, 119.0, 22.0 ],
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
					"patching_rect" : [ 450.0, 110.0, 102.0, 22.0 ],
					"text" : "prepend setMode"
				}
			},
			{
				"box" : 				{
					"id" : "obj-pack-ratio",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 140.0, 50.0, 22.0 ],
					"text" : "pack 2 3"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-ratio",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 170.0, 100.0, 22.0 ],
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
					"patching_rect" : [ 450.0, 200.0, 123.0, 22.0 ],
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
					"patching_rect" : [ 450.0, 230.0, 121.0, 22.0 ],
					"text" : "prepend setPitchLow"
				}
			},
			{
				"box" : 				{
					"id" : "obj-prepend-vel",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 260.0, 140.0, 22.0 ],
					"text" : "prepend setVelocityCurve"
				}
			}
		],
		"lines" : [
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-miditool-in", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-miditool-out", 0 ],
					"source" : [ "obj-js", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-dir", 0 ],
					"source" : [ "obj-direction", 0 ]
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
					"destination" : [ "obj-prepend-mode", 0 ],
					"source" : [ "obj-mode", 0 ]
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
					"destination" : [ "obj-pack-ratio", 0 ],
					"source" : [ "obj-ratio-num", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pack-ratio", 1 ],
					"source" : [ "obj-ratio-den", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-prepend-ratio", 0 ],
					"source" : [ "obj-pack-ratio", 0 ]
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
					"destination" : [ "obj-prepend-phigh", 0 ],
					"source" : [ "obj-pitch-high", 0 ]
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
					"destination" : [ "obj-prepend-plow", 0 ],
					"source" : [ "obj-pitch-low", 0 ]
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
					"destination" : [ "obj-prepend-vel", 0 ],
					"source" : [ "obj-velocity", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-js", 0 ],
					"source" : [ "obj-prepend-vel", 0 ]
				}
			}
		],
		"dependency_cache" : [
			{
				"name" : "risset.js",
				"bootpath" : "~/Github/risset/ableton",
				"patcherrelativepath" : "..",
				"type" : "TEXT",
				"implicit" : 1
			}
		],
		"autosave" : 0
	}
}
