import json
import pandas as pd
from typing import Union
from matplotlib.colors import LinearSegmentedColormap
from utils import update_dict_key
import plotly.express as px


cmap_input = Union[str, LinearSegmentedColormap]
plotly_cmap_default = px.colors.sequential.Tealgrn

class DecisionMaker:

    MIN_EVALUATION_FACTOR_IMPORTANCE = 0
    DEFAULT_EVALUATION_FACTOR_IMPORTANCE = 5
    MAX_EVALUATION_FACTOR_IMPORTANCE = 10
    MIN_DECISION_OPTION_VALUE = 0
    DEFAULT_DECISION_OPTION_VALUE = 5
    MAX_DECISION_OPTION_VALUE = 10
    def __init__(self):
        self.decision: str = ""
        self.decision_options_count: int = 2
        self.decision_options_list: list[str] = []
        self.evaluation_factors_count: int = 2
        self.evaluation_factors_list: list[str] = []
        self.evaluation_factor_importance_dict: dict[str, int] = {}
        self.decision_options_evaluation_dict: dict[str, dict[str, int]] = {}

        self.set_decision_options_count(self.decision_options_count)
        self.set_evaluation_factors_count(self.evaluation_factors_count)

        self.evaluation_factor_importance_df = pd.DataFrame()
        self.decision_options_evaluation_df = pd.DataFrame()
        self.decision_options_evaluation_adj_by_importance_df = pd.DataFrame()

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        repr_attrs = [
            'decision',
            'decision_options_count',
            'decision_options_list',
            'evaluation_factors_count',
            'evaluation_factors_list',
            'evaluation_factor_importance_dict',
            'decision_options_evaluation_dict'
        ]
        return {
            k: v for k, v in self.__dict__.items() if k in repr_attrs
        }

    def __str__(self):
        return f"Decision maker: `{self.decision}` " \
               f"with {self.decision_options_count} decision options " \
               f"and {self.evaluation_factors_count} evaluation factors."

    def __eq__(self, other) -> bool:
        if isinstance(other, DecisionMaker):
            return (
                self.decision == other.decision
                and self.decision_options_count == other.decision_options_count
                and self.decision_options_list == other.decision_options_list
                and self.evaluation_factors_count == other.evaluation_factors_count
                and self.evaluation_factors_list == other.evaluation_factors_list
                and self.evaluation_factor_importance_dict == other.evaluation_factor_importance_dict
                and self.decision_options_evaluation_dict == other.decision_options_evaluation_dict
                and self.evaluation_factor_importance_df.equals(other.evaluation_factor_importance_df)
                and self.decision_options_evaluation_df.equals(other.decision_options_evaluation_df)
            )
        return False

    def set_decision(self, value: str):
        self.decision = value

    def init_decision_options_count(self, value: int):
        self.decision_options_count = value
        self.set_decision_options_with_list([f"Option {i + 1}" for i in range(value)])

    def update_decision_options_count(self, value: int):
        old_value = self.decision_options_count
        self.decision_options_count = value
        self.decision_options_list = self.decision_options_list[: min(old_value, value)]
        self.decision_options_evaluation_dict = {
            k: v for k, v in self.decision_options_evaluation_dict.items()
            if k in self.decision_options_list
        }
        self.set_decision_options_with_list([
            f"Option {i + 1}" if (i + 1) > len(self.decision_options_list)
            else self.decision_options_list[i]
            for i in range(value)
        ])
        self.convert_decision_options_evaluation_dict_to_df()

    def set_decision_options_count(self, value: int):
        if not self.decision_options_list:
            self.init_decision_options_count(value)
            return
        self.update_decision_options_count(value)

    def init_decision_option(self, value: str):
        self.decision_options_list.append(value)
        self.decision_options_evaluation_dict[value] = {
            k: self.DEFAULT_DECISION_OPTION_VALUE
            for k in self.evaluation_factors_list
        }

    def update_decision_option(self, i: int, value: str):
        old_value = self.decision_options_list[i]
        self.decision_options_list[i] = value
        if value != old_value:
            self.decision_options_evaluation_dict = update_dict_key(
                dict_to_update=self.decision_options_evaluation_dict,
                old_key=old_value,
                new_key=value,
            )

    def set_decision_option(self, i: int, value: str):
        if (i + 1) > len(self.decision_options_list):
            self.init_decision_option(value)
            return
        self.update_decision_option(i, value)
        self.convert_decision_options_evaluation_dict_to_df()

    def set_decision_options_with_list(self, value_list: list[str]):
        assert len(value_list) == self.decision_options_count
        for i, value in enumerate(value_list):
            self.set_decision_option(i, value)

    def init_evaluation_factors_count(self, value: int):
        self.evaluation_factors_count = value
        self.set_evaluation_factors_with_list([f"Factor {i + 1}" for i in range(value)])

    def update_evaluation_factors_count(self, value: int):
        old_value = self.evaluation_factors_count
        self.evaluation_factors_count = value
        self.evaluation_factors_list = self.evaluation_factors_list[: min(old_value, value)]
        self.evaluation_factor_importance_dict = {
            k: v for k, v in self.evaluation_factor_importance_dict.items()
            if k in self.evaluation_factors_list
        }
        self.set_evaluation_factors_with_list([
            f"Factor {i + 1}" if (i + 1) > len(self.evaluation_factors_list)
            else self.evaluation_factors_list[i]
            for i in range(value)
        ])
        self.decision_options_evaluation_dict = {
            k: {
                evaluation_factor: ef_value
                for evaluation_factor, ef_value in v.items()
                if evaluation_factor in self.evaluation_factors_list
            }
            for k, v in self.decision_options_evaluation_dict.items()
        }
        self.convert_decision_options_evaluation_dict_to_df()

    def set_evaluation_factors_count(self, value: int):
        if not self.evaluation_factors_list:
            self.init_evaluation_factors_count(value)
            return
        self.update_evaluation_factors_count(value)

    def init_evaluation_factor(self, value: str):
        self.evaluation_factors_list.append(value)
        self.evaluation_factor_importance_dict[value] = self.DEFAULT_EVALUATION_FACTOR_IMPORTANCE
        self.decision_options_evaluation_dict = {
            k: {
                **v,
                **{value: self.DEFAULT_DECISION_OPTION_VALUE}
            }
            for k, v in self.decision_options_evaluation_dict.items()
        }

    def update_evaluation_factor(self, i: int, value: str):
        old_value = self.evaluation_factors_list[i]
        self.evaluation_factors_list[i] = value
        if value != old_value:
            self.evaluation_factor_importance_dict = update_dict_key(
                dict_to_update=self.evaluation_factor_importance_dict,
                old_key=old_value,
                new_key=value,
            )
        self.decision_options_evaluation_dict = {
            k: v if value == old_value else update_dict_key(
                dict_to_update=v,
                old_key=old_value,
                new_key=value,
            )
            for k, v in self.decision_options_evaluation_dict.items()
        }

    def set_evaluation_factor(self, i: int, value: str):
        if (i + 1) > len(self.evaluation_factors_list):
            self.init_evaluation_factor(value)
            return
        self.update_evaluation_factor(i, value)
        self.convert_dicts_to_df()

    def set_evaluation_factors_with_list(self, value_list: list[str]):
        assert len(value_list) == self.evaluation_factors_count
        for i, value in enumerate(value_list):
            self.set_evaluation_factor(i, value)

    def set_evaluation_factor_importance(self, i: int, value: int):
        self.evaluation_factor_importance_dict[
            self.evaluation_factors_list[i]
        ] = value
        self.convert_evaluation_factor_importance_dict_to_df()

    def set_evaluation_factor_importance_with_dict(self, value_dict: dict[str, int]):
        assert [
                   ef for ef in self.evaluation_factors_list if ef in value_dict.keys()
               ] == self.evaluation_factors_list
        for i, value in enumerate(value_dict.values()):
            self.set_evaluation_factor_importance(i, value)

    def set_decision_options_evaluation(self, i: int, k: int, value: int):
        self.decision_options_evaluation_dict[
            self.decision_options_list[i]
        ][self.evaluation_factors_list[k]] = value
        self.convert_decision_options_evaluation_dict_to_df()

    def set_decision_options_evaluation_with_dict(self, value_dict: dict[str, dict[str, int]]):
        assert [
                   do for do in self.decision_options_list if do in value_dict.keys()
               ] == self.decision_options_list
        for decision_option in self.decision_options_list:
            assert [
                       ef for ef in self.evaluation_factors_list
                       if ef in value_dict[decision_option].keys()
                   ] == self.evaluation_factors_list
        for i, decision_option in enumerate(value_dict.keys()):
            for k, evaluation_factor in enumerate(value_dict[decision_option].keys()):
                self.set_decision_options_evaluation(
                    i, k, value_dict[decision_option][evaluation_factor])

    def convert_evaluation_factor_importance_dict_to_df(self):
        self.evaluation_factor_importance_df = pd.DataFrame(
            self.evaluation_factor_importance_dict.values(),
            index=self.evaluation_factors_list,
            columns=['Importance'])

    def convert_decision_options_evaluation_dict_to_df(self):
        self.decision_options_evaluation_df = pd.DataFrame(
            self.decision_options_evaluation_dict)

    def convert_dicts_to_df(self):
        self.convert_evaluation_factor_importance_dict_to_df()
        self.convert_decision_options_evaluation_dict_to_df()

    def set_evaluation_factor_importance_df(self, df: pd.DataFrame):
        self.evaluation_factor_importance_df = df
        self.set_evaluation_factor_importance_with_dict(
            self.evaluation_factor_importance_df['Importance'].to_dict()
        )

    def set_decision_options_evaluation_df(self, df: pd.DataFrame):
        self.decision_options_evaluation_df = df
        self.set_decision_options_evaluation_with_dict(
            self.decision_options_evaluation_df.to_dict()
        )

    def compute_decision_options_evaluation_adj_by_importance_df(self):
        self.decision_options_evaluation_adj_by_importance_df = (
                self.decision_options_evaluation_df.mul(
                    self.evaluation_factor_importance_df['Importance'], axis=0
                ) / self.evaluation_factor_importance_df['Importance'].sum()
        )
        self.decision_options_evaluation_adj_by_importance_df.loc['Score'] = \
            self.decision_options_evaluation_adj_by_importance_df.sum()

    def compute_decision_score(self):
        self.decision_options_evaluation_df.loc['Score'] = (
                self.decision_options_evaluation_df.T.dot(
                    self.evaluation_factor_importance_df['Importance']
                ) / sum(list(self.evaluation_factor_importance_dict.values()))
        ).round(1).T

    def set_attributes(
            self,
            decision: str = "",
            decision_options_count: int = None,
            decision_options_list: list[str] = None,
            evaluation_factors_count: int = None,
            evaluation_factors_list: list[str] = None,
            evaluation_factor_importance_dict: dict[str, int] = None,
            decision_options_evaluation_dict: dict[str, dict[str, int]] = None,
    ):
        self.set_decision(decision)

        if not decision_options_count:
            return
        self.set_decision_options_count(decision_options_count)

        if not decision_options_list:
            return
        self.set_decision_options_with_list(decision_options_list)

        if not evaluation_factors_count:
            return
        self.set_evaluation_factors_count(evaluation_factors_count)

        if not evaluation_factors_list:
            return
        self.set_evaluation_factors_with_list(evaluation_factors_list)

        if not evaluation_factor_importance_dict:
            return
        self.set_evaluation_factor_importance_with_dict(evaluation_factor_importance_dict)

        if not decision_options_evaluation_dict:
            return
        self.set_decision_options_evaluation_with_dict(decision_options_evaluation_dict)

    def set_attributes_from(self, other):
        self.set_attributes(
            decision=other.decision,
            decision_options_count=other.decision_options_count,
            decision_options_list=other.decision_options_list,
            evaluation_factors_count=other.evaluation_factors_count,
            evaluation_factors_list=other.evaluation_factors_list,
            evaluation_factor_importance_dict=other.evaluation_factor_importance_dict,
            decision_options_evaluation_dict=other.decision_options_evaluation_dict,
        )

    def style_score_df(
            self,
            sort_ascending: bool = False,
            format_str: str = '{:.1f}',
            cmap: cmap_input = 'PuBu'
    ):
        return (
            self.decision_options_evaluation_df.T[['Score']]
            .sort_values('Score', ascending=sort_ascending)
            .style.format(format_str).background_gradient(cmap=cmap)
        )

    def plot_score(self, sort_ascending: bool = True, color_discrete_sequence: list[str] = plotly_cmap_default):
        fig = px.bar(
            self.decision_options_evaluation_df.T[['Score']].sort_values("Score", ascending=sort_ascending),
            x='Score', text='Score', orientation='h',
            labels={"index": "Decision option", "Score": "Decision score"},
            title="Decision options ranked by decision score",
            color_discrete_sequence=color_discrete_sequence,
        )
        fig.update_traces(textposition='outside', cliponaxis=False, textangle=0)

        return fig

    def style_decision_options_evaluation_df(
            self,
            sort_ascending: bool = False,
            format_str: str = '{:.1f}',
            cmap: cmap_input = 'PuBu'
    ):
        return (
            self.decision_options_evaluation_df.T
            .sort_values('Score', ascending=sort_ascending)
            .style.format({
                **{'Score': format_str},
                **{col: '{:.0f}'
                   for col in self.decision_options_evaluation_df.T.columns
                   if col != 'Score'}
            }).background_gradient(axis=None, cmap=cmap)
        )

    def plot_decision_options_evaluation_df(self, color_discrete_sequence: list[str] = plotly_cmap_default):
        fig = (
            self.decision_options_evaluation_df
            .drop(index=['Score']).plot.bar(
                barmode="group", text="value",
                labels=dict(index="Importance factor", value="Factor value", variable="Decision option"),
                color_discrete_sequence=color_discrete_sequence,
            )
        )
        fig.update_traces(textposition='outside', cliponaxis=False, textangle=0)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="auto",
            y=-0.5,
            xanchor="auto",
        ))
        return fig

    def style_decision_options_evaluation_adj_by_importance_df(
            self,
            format_str: str = '{:.1f}',
            cmap: cmap_input = 'PuBu'
    ):
        return (
            self.decision_options_evaluation_adj_by_importance_df
            .style.format(format_str).background_gradient(axis=None, cmap=cmap)
        )

    def plot_decision_options_evaluation_adj_by_importance_df(
            self, color_discrete_sequence: list[str] = plotly_cmap_default):
        fig = (
            self.decision_options_evaluation_adj_by_importance_df
            .drop(index=['Score']).T.round(1).plot.bar(
                text="value",
                labels=dict(index="Decision option", value="Factor value", variable="Importance factor"),
                color_discrete_sequence=color_discrete_sequence,
            )
        )
        fig.update_traces(textposition='inside', cliponaxis=False, textangle=0)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="auto",
            y=-1,
            xanchor="auto",
        ))
        return fig
