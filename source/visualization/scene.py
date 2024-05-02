import manim as mn
import pandas as pd
import json
import codecs


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


# Create a sample DataFrame
data = {
    "Name": ["John", "Jane", "Bob", "Alice"],
    "Category": ["A", "B", "A", "B"],
    "Value": ["10", "15", "20", "25"],
}


df = pd.DataFrame(
    data, columns=["Name", "Category", "Value"], index=["1", "2", "3", "4"]
)


class DataFrameTransformation(mn.Scene):
    def construct(self):

        text = (
            df.to_json(orient="records", lines=True)
            .replace('"', "")
            .replace("B", """<span foreground="red">B</span>""")
        )
        json_mobject = self.create_json(f"{text}")

        # describtion text
        descr_text = mn.MarkupText("Json File").scale(0.5).shift(mn.UP * 3.5)
        first_df = mn.MarkupText("First DataFrame").scale(0.5).shift(mn.UP * 3.5)
        transposed_df = (
            mn.MarkupText("Transposed DataFrame").scale(0.5).shift(mn.UP * 3.5)
        )

        # json_mobject = MarkupText('<span foreground="blue" size="x-large">Blue text</span> is <i>cool</i>!"')

        # Initial DataFrame table
        table = self.create_table(df)

        table.add(table.get_cell((2, 2), color=mn.RED))

        # Transform DataFrame to pivot table
        # pivot_table = df.pivot(index='Name', columns='Category', values='Value').fillna('0')
        transpose_table = df.T

        pivot_anim = self.create_table(df.T)
        pivot_anim.add(pivot_anim.get_cell((2, 2), color=mn.RED))

        # Create JSON Mobject

        # Play animation
        self.play(mn.Write(json_mobject), mn.Write(descr_text))

        self.wait(2)

        # Play the animation
        self.play(mn.Transform(json_mobject, table), mn.Transform(descr_text, first_df))

        # uncreate the result of the first animation
        # self.play(Uncreate(json_mobject))

        self.wait(2)
        self.play(
            mn.Transform(json_mobject, pivot_anim),
            mn.Transform(descr_text, transposed_df),
        )
        self.wait(2)

        # t0 = Table(
        #         [["This", "is asdf a"],
        #         ["simple", "Table in \n Manim."]])
        # self.play(Create(t0))

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

    def create_json(self, json_data):
        # Convert JSON data to a Manim Text Mobject

        return JSONMobject(json_data)
