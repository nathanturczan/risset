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
		"rect" : [ 100.0, 100.0, 1000.0, 750.0 ],
		"openinpresentation" : 1,
		"default_fontsize" : 10.0,
		"gridsize" : [ 15.0, 15.0 ],
		"description" : "Risset Rhythm Generator - Native UI",
		"digest" : "Generate polyrhythmic Risset rhythm patterns",
		"tags" : "MIDI Tool, Generator, Risset, Polyrhythm",
		"boxes" : [
			{
				"box" : 				{
					"comment" : "loadbang for initialization",
					"id" : "obj-loadbang",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 750.0, 20.0, 58.0, 20.0 ],
					"text" : "loadbang"
				}
			},
			{
				"box" : 				{
					"id" : "obj-init-trigger",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 5,
					"outlettype" : [ "bang", "bang", "bang", "bang", "bang" ],
					"patching_rect" : [ 750.0, 50.0, 180.0, 20.0 ],
					"text" : "t b b b b b"
				}
			},
			{
				"box" : 				{
					"id" : "obj-direction-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 20.0, 70.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 3.0, 65.0, 18.0 ],
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
					"presentation_rect" : [ 5.0, 18.0, 90.0, 20.0 ],
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
					"patching_rect" : [ 140.0, 20.0, 40.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 3.0, 40.0, 18.0 ],
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
					"patching_rect" : [ 140.0, 40.0, 60.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 20.0, 55.0, 15.0 ],
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
					"patching_rect" : [ 20.0, 80.0, 40.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 42.0, 40.0, 18.0 ],
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
					"patching_rect" : [ 20.0, 100.0, 36.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 57.0, 36.0, 15.0 ],
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
							"parameter_annotation" : "Numerator of the tempo ratio. For acceleration, should be smaller than denominator.",
							"parameter_annotation_name" : "Risset: Ratio Numerator"
						}
					},
					"varname" : "RatioNum"
				}
			},
			{
				"box" : 				{
					"id" : "obj-ratio-colon",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 58.0, 100.0, 15.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 42.0, 57.0, 10.0, 18.0 ],
					"text" : ":",
					"textjustification" : 1
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
					"patching_rect" : [ 75.0, 100.0, 36.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 53.0, 57.0, 36.0, 15.0 ],
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
							"parameter_annotation" : "Denominator of the tempo ratio. For acceleration, should be larger than numerator.",
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
					"patching_rect" : [ 130.0, 80.0, 55.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 42.0, 55.0, 18.0 ],
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
					"patching_rect" : [ 130.0, 100.0, 36.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 57.0, 36.0, 15.0 ],
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
					"id" : "obj-pitch-high-note",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 170.0, 100.0, 30.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 138.0, 57.0, 25.0, 18.0 ],
					"text" : "E3",
					"textcolor" : [ 0.6, 0.6, 0.6, 1.0 ],
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-low-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 130.0, 125.0, 60.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 75.0, 60.0, 18.0 ],
					"text" : "LOW (OUT)",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-pitch-low",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 130.0, 145.0, 36.0, 15.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 100.0, 90.0, 36.0, 15.0 ],
					"maxclass" : "live.numbox",
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
					"id" : "obj-pitch-low-note",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 170.0, 145.0, 30.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 138.0, 90.0, 25.0, 18.0 ],
					"text" : "C3",
					"textcolor" : [ 0.6, 0.6, 0.6, 1.0 ],
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-velocity-label",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 175.0, 120.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 110.0, 155.0, 18.0 ],
					"text" : "VELOCITY RESPONSE",
					"textjustification" : 0
				}
			},
			{
				"box" : 				{
					"id" : "obj-velocity",
					"maxclass" : "live.slider",
					"numinlets" : 1,
					"numoutlets" : 2,
					"orientation" : 1,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 20.0, 195.0, 140.0, 19.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 125.0, 155.0, 19.0 ],
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
					"id" : "obj-velocity-punch",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 216.0, 35.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 144.0, 35.0, 18.0 ],
					"text" : "Punch",
					"textcolor" : [ 0.5, 0.5, 0.5, 1.0 ],
					"textjustification" : 0,
					"fontsize" : 9.0
				}
			},
			{
				"box" : 				{
					"id" : "obj-velocity-gentle",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 125.0, 216.0, 35.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 125.0, 144.0, 35.0, 18.0 ],
					"text" : "Gentle",
					"textcolor" : [ 0.5, 0.5, 0.5, 1.0 ],
					"textjustification" : 2,
					"fontsize" : 9.0
				}
			},
			{
				"box" : 				{
					"id" : "obj-constraint",
					"maxclass" : "live.comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 245.0, 180.0, 18.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 162.0, 155.0, 18.0 ],
					"text" : "2:3  Num < Den",
					"textcolor" : [ 1.0, 0.42, 0.21, 1.0 ],
					"textjustification" : 0,
					"fontsize" : 10.0
				}
			},
			{
				"box" : 				{
					"id" : "obj-miditool-in",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 300.0, 50.0, 100.0, 20.0 ],
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
					"patching_rect" : [ 300.0, 150.0, 80.0, 20.0 ],
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
					"patching_rect" : [ 300.0, 200.0, 105.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 80.0, 119.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 110.0, 102.0, 20.0 ],
					"text" : "prepend setMode"
				}
			},
			{
				"box" : 				{
					"comment" : "Constraint enforcer - ensures valid ratio for direction",
					"id" : "obj-constraint-js",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 450.0, 170.0, 100.0, 20.0 ],
					"saved_object_attributes" : 					{
						"filename" : "constraint.js",
						"parameter_enable" : 0
					},
					"text" : "js constraint.js"
				}
			},
			{
				"box" : 				{
					"id" : "obj-pack-ratio",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 210.0, 50.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 240.0, 100.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 300.0, 123.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 330.0, 121.0, 20.0 ],
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
					"patching_rect" : [ 450.0, 360.0, 140.0, 20.0 ],
					"text" : "prepend setVelocityCurve"
				}
			},
			{
				"box" : 				{
					"comment" : "Convert MIDI pitch to note name for high",
					"id" : "obj-mton-high",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 620.0, 300.0, 35.0, 20.0 ],
					"text" : "mton"
				}
			},
			{
				"box" : 				{
					"comment" : "Convert MIDI pitch to note name for low",
					"id" : "obj-mton-low",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 620.0, 330.0, 35.0, 20.0 ],
					"text" : "mton"
				}
			},
			{
				"box" : 				{
					"comment" : "Set high pitch note name",
					"id" : "obj-set-high-note",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 660.0, 300.0, 68.0, 20.0 ],
					"text" : "prepend set"
				}
			},
			{
				"box" : 				{
					"comment" : "Set low pitch note name",
					"id" : "obj-set-low-note",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 660.0, 330.0, 68.0, 20.0 ],
					"text" : "prepend set"
				}
			},
			{
				"box" : 				{
					"comment" : "Set numbox without triggering output",
					"id" : "obj-set-num",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 560.0, 170.0, 68.0, 20.0 ],
					"text" : "prepend set"
				}
			},
			{
				"box" : 				{
					"comment" : "Set numbox without triggering output",
					"id" : "obj-set-den",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 560.0, 200.0, 68.0, 20.0 ],
					"text" : "prepend set"
				}
			},
			{
				"box" : 				{
					"comment" : "Store direction for constraint text",
					"id" : "obj-dir-store",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 450.0, 420.0, 29.5, 20.0 ],
					"text" : "i 0"
				}
			},
			{
				"box" : 				{
					"comment" : "Trigger constraint text update",
					"id" : "obj-text-trigger",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "bang" ],
					"patching_rect" : [ 450.0, 450.0, 32.0, 20.0 ],
					"text" : "t b b"
				}
			},
			{
				"box" : 				{
					"comment" : "Store corrected num for text",
					"id" : "obj-num-store",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 450.0, 480.0, 29.5, 20.0 ],
					"text" : "i 2"
				}
			},
			{
				"box" : 				{
					"comment" : "Store corrected den for text",
					"id" : "obj-den-store",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 490.0, 480.0, 29.5, 20.0 ],
					"text" : "i 3"
				}
			},
			{
				"box" : 				{
					"comment" : "Select direction for symbol",
					"id" : "obj-dir-select",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 3,
					"outlettype" : [ "bang", "bang", "" ],
					"patching_rect" : [ 530.0, 480.0, 52.0, 20.0 ],
					"text" : "select 0 1"
				}
			},
			{
				"box" : 				{
					"comment" : "Accel symbol message",
					"id" : "obj-accel-msg",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 530.0, 510.0, 30.0, 20.0 ],
					"text" : "<"
				}
			},
			{
				"box" : 				{
					"comment" : "Decel symbol message",
					"id" : "obj-decel-msg",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 565.0, 510.0, 30.0, 20.0 ],
					"text" : ">"
				}
			},
			{
				"box" : 				{
					"comment" : "Constraint text formatter",
					"id" : "obj-constraint-format",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 450.0, 550.0, 180.0, 20.0 ],
					"text" : "sprintf set %d:%d  Num %s Den"
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
					"destination" : [ "obj-constraint-js", 0 ],
					"source" : [ "obj-direction", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dir-store", 1 ],
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
					"destination" : [ "obj-constraint-js", 1 ],
					"source" : [ "obj-ratio-num", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint-js", 2 ],
					"source" : [ "obj-ratio-den", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pack-ratio", 0 ],
					"source" : [ "obj-constraint-js", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-set-num", 0 ],
					"source" : [ "obj-constraint-js", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-num-store", 1 ],
					"source" : [ "obj-constraint-js", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-text-trigger", 0 ],
					"source" : [ "obj-constraint-js", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pack-ratio", 1 ],
					"source" : [ "obj-constraint-js", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-set-den", 0 ],
					"source" : [ "obj-constraint-js", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-den-store", 1 ],
					"source" : [ "obj-constraint-js", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-ratio-num", 0 ],
					"source" : [ "obj-set-num", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-ratio-den", 0 ],
					"source" : [ "obj-set-den", 0 ]
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
					"destination" : [ "obj-mton-high", 0 ],
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
					"destination" : [ "obj-mton-low", 0 ],
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
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-set-high-note", 0 ],
					"source" : [ "obj-mton-high", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pitch-high-note", 0 ],
					"source" : [ "obj-set-high-note", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-set-low-note", 0 ],
					"source" : [ "obj-mton-low", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pitch-low-note", 0 ],
					"source" : [ "obj-set-low-note", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-num-store", 0 ],
					"source" : [ "obj-text-trigger", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dir-store", 0 ],
					"source" : [ "obj-text-trigger", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint-format", 0 ],
					"source" : [ "obj-num-store", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint-format", 1 ],
					"source" : [ "obj-den-store", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dir-select", 0 ],
					"source" : [ "obj-dir-store", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-accel-msg", 0 ],
					"source" : [ "obj-dir-select", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-decel-msg", 0 ],
					"source" : [ "obj-dir-select", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint-format", 2 ],
					"source" : [ "obj-accel-msg", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint-format", 2 ],
					"source" : [ "obj-decel-msg", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-constraint", 0 ],
					"source" : [ "obj-constraint-format", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-init-trigger", 0 ],
					"source" : [ "obj-loadbang", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-direction", 0 ],
					"source" : [ "obj-init-trigger", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-mode", 0 ],
					"source" : [ "obj-init-trigger", 1 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pitch-high", 0 ],
					"source" : [ "obj-init-trigger", 2 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pitch-low", 0 ],
					"source" : [ "obj-init-trigger", 3 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-velocity", 0 ],
					"source" : [ "obj-init-trigger", 4 ]
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
			},
			{
				"name" : "constraint.js",
				"bootpath" : "~/Github/risset/ableton/native-ui",
				"patcherrelativepath" : ".",
				"type" : "TEXT",
				"implicit" : 1
			}
		],
		"autosave" : 0
	}
}
