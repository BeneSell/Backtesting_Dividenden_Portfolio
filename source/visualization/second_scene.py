import manim as mn
import pandas as pd
import json
import codecs
import data_preprocessing.preproccess_classes as pre

import sys

class JSONMobject(mn.VGroup):
    def __init__(self, json_data, **kwargs):
        super().__init__(**kwargs)
        # self.json_data = f"{json_data}"
        # self.json_data = bytes(json_data, "utf-8").decode("unicode_escape")
        self.json_data = json_data
        self.create_json_mobject()

    def create_json_mobject(self):
        # Convert JSON data to a Manim Text Mobject
        # json_text = json.dumps(self.json_data, indent=2)

        # json_text = str.replace(self.json_data, "\n", "\\n")
        json_mobject = mn.MarkupText(self.json_data, font="Consolas").scale(0.5)
        self.add(json_mobject)





class DataFrameTransformation(mn.Scene):
    
    def get_data(self):
        with open('../data/stock_infos/raw_data_fmp.json', "r") as json_file:
            raw_data_fmp_dividends = json.load(json_file)

        with open('../data/stock_infos/raw_data_fmp_stock_value.json', "r") as json_file:
            raw_data_fmp_stock_value = json.load(json_file)

        with open('../data/stock_infos/result.json') as json_file:
            data = json_file.read()
            raw_data_alpha = json.loads(data)


        pre_fmp = pre.preproccessing_fmp_data(raw_data_fmp_dividends[:5], raw_data_fmp_stock_value[:5])
        pre_alpha = pre.preproccessing_alphavantage_data(raw_data_alpha[:5])

        return pre_fmp, pre_alpha

    def construct(self):

        self.pre_fmp, self.pre_alpha = self.get_data()

        
        df = self.pre_fmp.normalized_data_dividend.head(5)

        # convert every value to string
        # for showing data you only need strings
        df = df.map(lambda x: str(x))

        print(df)

        text = df.to_json(orient='records', lines=True, default_handler=str)
        #     .replace("\"", "").replace("B", """<span foreground="red">B</span>""")
        json_mobject = mn.MarkupText(f'{text}', font="Consolas").scale(0.5)

        # describtion text
        descr_text = mn.MarkupText("Json File").scale(0.5).shift(mn.UP*3.5)
        first_df = mn.MarkupText("First DataFrame").scale(0.5).shift(mn.UP*3.5)
        transposed_df = mn.MarkupText("Transposed DataFrame").scale(0.5).shift(mn.UP*3.5)

        

        # Initial DataFrame table
        table = self.create_table(df)
        table.add(table.get_cell((2,2), color=mn.RED))
        
        
        
        pivot_anim = self.create_table(self.pre_fmp.pivot_dividenden_data(df))
        

        # custom animations
        pivot_anim.add(pivot_anim.get_cell((2,2), color=mn.RED))

        
        self.play(mn.Write(descr_text))
        self.play(mn.Write(json_mobject))
        self.wait(2)
        self.animate_from_to_with_description(json_mobject, table, descr_text, first_df)
        
        self.animate_from_to_with_description(json_mobject, pivot_anim, descr_text, transposed_df)

        
        

       

    def animate_from_to_with_description(self, from_mobject: mn.Mobject, to_mobject: mn.Mobject, start_description, new_description):

        
        self.play(mn.Transform(from_mobject, to_mobject), 
                  mn.Transform(start_description, new_description))
        self.wait(2)


    def create_table(self, dataframe):

        print(dataframe.index.tolist())

        # Convert DataFrame to Manim Table
        table = mn.Table(
            dataframe.values.tolist(),
            # row_labels=dataframe.index.tolist(),
            # col_labels=dataframe.columns.tolist(),
            include_outer_lines=True,
            # include_inner_lines=True,
            h_buff=0.7,
            v_buff=0.4,
            # cell_width_proportion=1.5
        )

        return table
