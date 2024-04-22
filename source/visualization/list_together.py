import manim as mn
import pandas as pd
import json
import codecs
# import data_preprocessing.preproccess_classes as pre

import sys

yield_data =    [{'company':"Apple", "yield": "11"},
                {'company': "Microsoft", "yield": "2"},
                {'company': "Netflix", "yield": "3"},
                {'company': "Adobe", "yield": "4"},
                {'company': "Pizza Hut", "yield": "5"},
                {'company': "Netflix", "yield": "6"},
                {'company': "DM", "yield": "7"},
                {'company': "Ricola", "yield": "8"}]

growth_data = [{'company':  "Apple", "growth": "1.07"},
                {'company': "Microsoft", "growth": "1.61"},
                {'company': "Netflix", "growth": "1.52"},
                {'company': "Adobe", "growth": "1.43"},
                {'company': "Pizza Hut", "growth": "1.34"},
                {'company': "Netflix", "growth": "1.25"},
                {'company': "DM", "growth": "1.16"},
                {'company': "Ricola", "growth": "1.07"}]

stability_data =[{'company':"Apple", "stability": "071.07"},
                {'company': "Microsoft", "stability": "611.61"},
                {'company': "Netflix", "stability": "521.52"},
                {'company': "Adobe", "stability": "431.43"},
                {'company': "Pizza Hut", "stability": "341.34"},
                {'company': "Netflix", "stability": "251.25"},
                {'company': "DM", "stability": "161.16"},
                {'company': "Ricola", "stability": "070.07"}]








class DataFrameTransformation(mn.Scene):
    
    def get_data(self):

        yield_df = pd.DataFrame(yield_data)
        yield_df["rank_yield"] = yield_df["yield"].rank(ascending=False)
        growth_df = pd.DataFrame(growth_data)
        growth_df["rank_growth"] = growth_df["growth"].rank(ascending=False)
        stability_df = pd.DataFrame(stability_data)
        stability_df["rank_stability"] = stability_df["stability"].rank(ascending=False)

        return yield_df, growth_df, stability_df

    def construct(self):

        yiled_df, growth_df, stability_df = self.get_data()


        # combine df on date
        combined_df = pd.concat([yiled_df, growth_df, stability_df], axis=0)
        print(combined_df)
        grouped_df = combined_df.groupby("company").sum().reset_index()
        grouped_df["rank"] = grouped_df["rank_growth"].astype(float) + grouped_df["rank_yield"].astype(float) + grouped_df["rank_stability"].astype(float)
        
        
        grouped_df = grouped_df[["company", "rank"]].sort_values(by="rank", ascending=True)
        grouped_df["rank"] = grouped_df["rank"].astype(str)

        
        

        # convert every value to string
        # for showing data you only need strings
        
        yiled_df = yiled_df.map(lambda x: str(x))
        growth_df = growth_df.map(lambda x: str(x))
        stability_df = stability_df.map(lambda x: str(x))

        
        # describtion text
        descr_text = mn.MarkupText("All Rankings").scale(0.5).shift(mn.UP*3.5)
        first_df = mn.MarkupText("Combined them").scale(0.5).shift(mn.UP*3.5)
        transposed_df = mn.MarkupText("Transposed DataFrame").scale(0.5).shift(mn.UP*3.5)

        

        # Initial DataFrame table
        yield_animated = self.create_table(yiled_df)
        growth_animated = self.create_table(growth_df)
        stability_animated = self.create_table(stability_df)

        # table.add(table.get_cell((2,2), color=mn.RED))
        
        
        
        grouped_df_animated = self.create_table(grouped_df).scale(0.5)
        grouped_df_animated.add(mn.SurroundingRectangle(grouped_df_animated.get_columns()[1]))        

        # custom animations
        # pivot_anim.add(pivot_anim.get_cell((2,2), color=mn.RED))

        
        self.play(mn.Write(descr_text)),mn.Write(yield_animated.shift(mn.RIGHT*4).scale(0.25)),mn.Write(growth_animated.scale(0.25)),mn.Write(stability_animated.shift(mn.LEFT*4.5).scale(0.25))

        # mark the second column red
        yield_animated.add(mn.SurroundingRectangle(yield_animated.get_columns()[2]))
        growth_animated.add(mn.SurroundingRectangle(growth_animated.get_columns()[2]))
        stability_animated.add(mn.SurroundingRectangle(stability_animated.get_columns()[2]))

        # change data of stability_animated
        # stability_animated.change_values(stability_df.sort_values(by="rank_stability").values.tolist())

        self.wait(2)

        # do a pop up animation with text "sort them by rank and combine them"
        self.play(mn.FadeOut(mn.MarkupText("Sort them by rank").scale(0.8).shift(mn.UP*1.5)))


        self.play(mn.Transform(yield_animated, self.create_table(yiled_df.sort_values(by="rank_yield")).shift(mn.RIGHT*4).scale(0.25).add(mn.SurroundingRectangle(yield_animated.get_columns()[2]))),
                    mn.Transform(growth_animated, self.create_table(growth_df.sort_values(by="rank_growth")).scale(0.25).add(mn.SurroundingRectangle(growth_animated.get_columns()[2]))),
                    mn.Transform(stability_animated, self.create_table(stability_df.sort_values(by="rank_stability")).shift(mn.LEFT*4.5).scale(0.25).add(mn.SurroundingRectangle(stability_animated.get_columns()[2]))))

        self.wait(2)
        # remove yield and growth
        self.play(mn.FadeOut(yield_animated), mn.FadeOut(growth_animated))
        
        self.animate_from_to_with_description(stability_animated, grouped_df_animated, descr_text, first_df)
        
        # self.animate_from_to_with_description(json_mobject, pivot_anim, descr_text, transposed_df)

        
        

       

    def animate_from_to_with_description(self, from_mobject: mn.Mobject, to_mobject: mn.Mobject, start_description, new_description):

        
        self.play(mn.Transform(from_mobject, to_mobject), 
                  mn.Transform(start_description, new_description))
        self.wait(2)


    def create_table(self, dataframe):

        # print(dataframe.index.tolist())

        values_for_table = [dataframe.columns] + dataframe.values.tolist()

        # Convert DataFrame to Manim Table
        table = mn.Table(
            values_for_table,
            # row_labels=dataframe.index.tolist(),
            # col_labels=dataframe.columns.tolist(),
            include_outer_lines=True,
            # include_inner_lines=True,
            h_buff=0.7,
            v_buff=0.4,
            # cell_width_proportion=1.5
        )

        return table
