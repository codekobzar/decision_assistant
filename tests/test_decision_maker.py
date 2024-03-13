import pandas as pd
import pytest

from decision_maker import DecisionMaker


@pytest.fixture
def example_decision():
    return "What is the best way to take decisions?"


@pytest.fixture
def example_decision_options_list():
    return [
        "Flip a coin",
        "Listen to your heart",
        "Hire a consultant",
        "Use decision maker"
    ]


@pytest.fixture
def example_decision_options_list_w_new_decision_option():
    return [
        "Flip a coin",
        "Ask friends",
        "Hire a consultant",
        "Use decision maker"
    ]


@pytest.fixture
def example_evaluation_factors_list():
    return [
        "Speed",
        "Quality",
        "Cost",
        "Certainty"
    ]


@pytest.fixture
def example_evaluation_factors_list_w_new_evaluation_factor():
    return [
        "Speed",
        "Relevance",
        "Cost",
        "Certainty"
    ]


@pytest.fixture
def example_evaluation_factor_importance_dict():
    return {
        "Speed": 4,
        "Quality": 9,
        "Cost": 2,
        "Certainty": 6
    }


@pytest.fixture
def example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance():
    return {
        "Speed": 10,
        "Quality": 9,
        "Cost": 2,
        "Certainty": 6
    }


@pytest.fixture
def example_evaluation_factor_importance_dict_w_new_evaluation_factor():
    return {
        "Speed": 4,
        "Relevance": 9,
        "Cost": 2,
        "Certainty": 6
    }


@pytest.fixture
def example_decision_options_evaluation_dict():
    return {
        "Flip a coin": {
            "Speed": 10,
            "Quality": 2,
            "Cost": 9,
            "Certainty": 8
        },
        "Listen to your heart": {
            "Speed": 2,
            "Quality": 7,
            "Cost": 10,
            "Certainty": 6
        },
        "Hire a consultant": {
            "Speed": 5,
            "Quality": 8,
            "Cost": 0,
            "Certainty": 4
        },
        "Use decision maker": {
            "Speed": 8,
            "Quality": 8,
            "Cost": 9,
            "Certainty": 9
        }
    }


@pytest.fixture
def example_decision_options_evaluation_dict_w_new_evaluation_factor():
    return {
        "Flip a coin": {
            "Speed": 10,
            "Relevance": 2,
            "Cost": 9,
            "Certainty": 8
        },
        "Listen to your heart": {
            "Speed": 2,
            "Relevance": 7,
            "Cost": 10,
            "Certainty": 6
        },
        "Hire a consultant": {
            "Speed": 5,
            "Relevance": 8,
            "Cost": 0,
            "Certainty": 4
        },
        "Use decision maker": {
            "Speed": 8,
            "Relevance": 8,
            "Cost": 9,
            "Certainty": 9
        }
    }


@pytest.fixture
def example_decision_options_evaluation_dict_w_new_decision_option():
    return {
        "Flip a coin": {
            "Speed": 10,
            "Quality": 2,
            "Cost": 9,
            "Certainty": 8
        },
        "Ask friends": {
            "Speed": 2,
            "Quality": 7,
            "Cost": 10,
            "Certainty": 6
        },
        "Hire a consultant": {
            "Speed": 5,
            "Quality": 8,
            "Cost": 0,
            "Certainty": 4
        },
        "Use decision maker": {
            "Speed": 8,
            "Quality": 8,
            "Cost": 9,
            "Certainty": 9
        }
    }


@pytest.fixture
def example_decision_options_evaluation_dict_w_new_decision_option_evaluation():
    return {
        "Flip a coin": {
            "Speed": 10,
            "Quality": 2,
            "Cost": 9,
            "Certainty": 8
        },
        "Listen to your heart": {
            "Speed": 6,
            "Quality": 7,
            "Cost": 10,
            "Certainty": 6
        },
        "Hire a consultant": {
            "Speed": 5,
            "Quality": 8,
            "Cost": 0,
            "Certainty": 4
        },
        "Use decision maker": {
            "Speed": 8,
            "Quality": 8,
            "Cost": 9,
            "Certainty": 9
        }
    }

@pytest.fixture
def example_evaluation_factor_importance_df(example_evaluation_factor_importance_dict):
    return pd.DataFrame(
        list(example_evaluation_factor_importance_dict.values()),
        index=list(example_evaluation_factor_importance_dict.keys()), columns=['Importance']
    )

@pytest.fixture
def example_evaluation_factor_importance_df_w_new_evaluation_factor_importance(
        example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance):
    return pd.DataFrame(
        list(example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance.values()),
        index=list(example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance.keys()),
        columns=['Importance']
    )

@pytest.fixture
def example_decision_options_evaluation_df(
        example_evaluation_factor_importance_dict,
        example_decision_options_list
):
    # evaluation factor values for different decision options - inner arrays
    # decision options - outer arrays
    return pd.DataFrame(
        [[10, 2, 5, 8], [2, 7, 8, 8], [9, 10, 0, 9], [8, 6, 4, 9]],
        index=list(example_evaluation_factor_importance_dict.keys()),
        columns=example_decision_options_list
    )

@pytest.fixture
def example_decision_options_evaluation_df_w_new_decision_option_evaluation(
        example_evaluation_factor_importance_dict,
        example_decision_options_list
):
    return pd.DataFrame(
        [[10, 6, 5, 8], [2, 7, 8, 8], [9, 10, 0, 9], [8, 6, 4, 9]],
        index=list(example_evaluation_factor_importance_dict.keys()),
        columns=example_decision_options_list
    )

@pytest.fixture
def example_scores(example_decision_options_list):
    return pd.DataFrame(
        [5.9, 6.0, 5.5, 8.4],
        index=example_decision_options_list,
        columns=['Score']
    )

@pytest.fixture
def example_decision_maker_without_evaluation(
        example_decision,
        example_decision_options_list,
        example_evaluation_factors_list,
        example_evaluation_factor_importance_dict
):
    decision_maker = DecisionMaker()
    decision_maker.set_attributes(
        decision=example_decision,
        decision_options_count=len(example_decision_options_list),
        decision_options_list=example_decision_options_list,
        evaluation_factors_count=len(example_evaluation_factors_list),
        evaluation_factors_list=example_evaluation_factors_list,
        evaluation_factor_importance_dict=example_evaluation_factor_importance_dict
    )
    return decision_maker

@pytest.fixture
def example_decision_maker(
        example_decision_maker_without_evaluation,
        example_decision_options_evaluation_dict
):
    decision_maker = example_decision_maker_without_evaluation
    decision_maker.set_decision_options_evaluation_with_dict(example_decision_options_evaluation_dict)
    return decision_maker

class TestDecisionMaker:
    decision_maker = DecisionMaker()

    def test_set_decision_options_count(self, example_decision_options_list):
        self.decision_maker.set_decision_options_count(len(example_decision_options_list))
        assert self.decision_maker.decision_options_count == len(self.decision_maker.decision_options_list)

    def test_set_decision_option(self, example_decision_options_list):
        self.decision_maker.set_decision_options_count(len(example_decision_options_list))
        self.decision_maker.set_decision_options_with_list(example_decision_options_list)
        assert self.decision_maker.decision_options_list == example_decision_options_list

    def test_set_evaluation_factors_count(self, example_evaluation_factors_list):
        self.decision_maker.set_evaluation_factors_count(len(example_evaluation_factors_list))
        assert self.decision_maker.evaluation_factors_count == len(self.decision_maker.evaluation_factors_list)

    def test_set_evaluation_factor(self, example_evaluation_factors_list):
        self.decision_maker.set_evaluation_factors_count(len(example_evaluation_factors_list))
        self.decision_maker.set_evaluation_factors_with_list(example_evaluation_factors_list)
        assert self.decision_maker.evaluation_factors_list == example_evaluation_factors_list

    def test_set_evaluation_factor_importance(self, example_evaluation_factor_importance_dict):
        self.decision_maker.set_evaluation_factors_count(len(example_evaluation_factor_importance_dict.keys()))
        self.decision_maker.set_evaluation_factors_with_list(list(example_evaluation_factor_importance_dict.keys()))
        self.decision_maker.set_evaluation_factor_importance_with_dict(example_evaluation_factor_importance_dict)
        assert self.decision_maker.evaluation_factor_importance_dict == example_evaluation_factor_importance_dict

    def test_set_decision_options_evaluation(
            self,
            example_decision_options_evaluation_dict,
            example_decision_maker_without_evaluation
    ):
        decision_maker = example_decision_maker_without_evaluation
        decision_maker.set_decision_options_evaluation_with_dict(example_decision_options_evaluation_dict)
        assert decision_maker.decision_options_evaluation_dict == example_decision_options_evaluation_dict

    def test_convert_evaluation_factor_importance_dict_to_df(
            self,
            example_decision_maker,
            example_evaluation_factor_importance_df
    ):
        example_decision_maker.convert_evaluation_factor_importance_dict_to_df()
        assert example_decision_maker.evaluation_factor_importance_df.equals(
            example_evaluation_factor_importance_df)

    def test_convert_decision_options_evaluation_dict_to_df(
            self,
            example_decision_maker,
            example_decision_options_evaluation_df
    ):
        example_decision_maker.convert_decision_options_evaluation_dict_to_df()
        assert example_decision_maker.decision_options_evaluation_df.equals(
            example_decision_options_evaluation_df)

    def test_compute_decision_options_evaluation_adj_by_importance_df(
            self,
            example_decision_maker,
            example_scores
    ):
        example_decision_maker.compute_decision_options_evaluation_adj_by_importance_df()
        assert example_decision_maker.decision_options_evaluation_adj_by_importance_df.loc["Score"].round(1).equals(
            example_scores['Score']
        )

    def test_compute_decision_score(
            self,
            example_decision_maker,
            example_scores
    ):
        example_decision_maker.compute_decision_score()
        assert example_decision_maker.decision_options_evaluation_df.loc["Score"].round(1).equals(
            example_scores['Score']
        )

    def test_update_evaluation_factor(
            self,
            example_decision_maker,
            example_evaluation_factors_list_w_new_evaluation_factor,
            example_evaluation_factor_importance_dict_w_new_evaluation_factor,
            example_decision_options_evaluation_dict_w_new_evaluation_factor
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=example_decision_maker.decision_options_count,
            decision_options_list=example_decision_maker.decision_options_list,
            evaluation_factors_count=len(example_evaluation_factors_list_w_new_evaluation_factor),
            evaluation_factors_list=example_evaluation_factors_list_w_new_evaluation_factor,
            evaluation_factor_importance_dict=example_evaluation_factor_importance_dict_w_new_evaluation_factor,
            decision_options_evaluation_dict=example_decision_options_evaluation_dict_w_new_evaluation_factor
        )

        decision_maker_old.set_evaluation_factors_with_list(example_evaluation_factors_list_w_new_evaluation_factor)

        assert decision_maker_old == decision_maker_new

    def test_update_decision_option(
            self,
            example_decision_maker,
            example_decision_options_list_w_new_decision_option,
            example_decision_options_evaluation_dict_w_new_decision_option
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=len(example_decision_options_list_w_new_decision_option),
            decision_options_list=example_decision_options_list_w_new_decision_option,
            evaluation_factors_count=len(example_decision_maker.evaluation_factors_list),
            evaluation_factors_list=example_decision_maker.evaluation_factors_list,
            evaluation_factor_importance_dict=example_decision_maker.evaluation_factor_importance_dict,
            decision_options_evaluation_dict=example_decision_options_evaluation_dict_w_new_decision_option
        )

        decision_maker_old.set_decision_options_with_list(example_decision_options_list_w_new_decision_option)

        assert decision_maker_old == decision_maker_new

    def test_update_decision_options_count(
            self,
            example_decision_maker,
            decision_options_count_change: int = -2
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        updated_decision_options_count = example_decision_maker.decision_options_count + decision_options_count_change
        updated_decision_options_list = example_decision_maker.decision_options_list[:updated_decision_options_count]
        updated_decision_options_evaluation = {
            k: v for k, v in example_decision_maker.decision_options_evaluation_dict.items()
            if k in updated_decision_options_list
        }
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=updated_decision_options_count,
            decision_options_list=updated_decision_options_list,
            evaluation_factors_count=len(example_decision_maker.evaluation_factors_list),
            evaluation_factors_list=example_decision_maker.evaluation_factors_list,
            evaluation_factor_importance_dict=example_decision_maker.evaluation_factor_importance_dict,
            decision_options_evaluation_dict=updated_decision_options_evaluation
        )

        decision_maker_old.set_decision_options_count(updated_decision_options_count)

        assert decision_maker_old == decision_maker_new

    def test_update_evaluation_factors_count(
            self,
            example_decision_maker,
            evaluation_factors_count_change: int = -2
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        updated_evaluation_factors_count = example_decision_maker.evaluation_factors_count + evaluation_factors_count_change
        updated_evaluation_factors_list = example_decision_maker.evaluation_factors_list[:updated_evaluation_factors_count]
        updated_evaluation_factors_importance = {
            k: v for k, v in example_decision_maker.evaluation_factor_importance_dict.items()
            if k in updated_evaluation_factors_list
        }
        updated_decision_options_evaluation = {
            k: {
                evaluation_factor: ef_value
                for evaluation_factor, ef_value in v.items()
                if evaluation_factor in updated_evaluation_factors_list
            }
            for k, v in example_decision_maker.decision_options_evaluation_dict.items()
        }
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=example_decision_maker.decision_options_count,
            decision_options_list=example_decision_maker.decision_options_list,
            evaluation_factors_count=updated_evaluation_factors_count,
            evaluation_factors_list=updated_evaluation_factors_list,
            evaluation_factor_importance_dict=updated_evaluation_factors_importance,
            decision_options_evaluation_dict=updated_decision_options_evaluation
        )

        decision_maker_old.set_evaluation_factors_count(updated_evaluation_factors_count)

        assert decision_maker_old == decision_maker_new

    def test_set_evaluation_factor_importance_df(
            self,
            example_decision_maker,
            example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance,
            example_evaluation_factor_importance_df_w_new_evaluation_factor_importance
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=example_decision_maker.decision_options_count,
            decision_options_list=example_decision_maker.decision_options_list,
            evaluation_factors_count=example_decision_maker.evaluation_factors_count,
            evaluation_factors_list=example_decision_maker.evaluation_factors_list,
            evaluation_factor_importance_dict=example_evaluation_factor_importance_dict_w_new_evaluation_factor_importance,
            decision_options_evaluation_dict=example_decision_maker.decision_options_evaluation_dict
        )

        decision_maker_old.set_evaluation_factor_importance_df(
            example_evaluation_factor_importance_df_w_new_evaluation_factor_importance)

        assert decision_maker_old == decision_maker_new

    def test_set_decision_options_evaluation_df(
            self,
            example_decision_maker,
            example_decision_options_evaluation_dict_w_new_decision_option_evaluation,
            example_decision_options_evaluation_df_w_new_decision_option_evaluation
    ):
        decision_maker_old = example_decision_maker
        decision_maker_new = DecisionMaker()
        decision_maker_new.set_attributes(
            decision=example_decision_maker.decision,
            decision_options_count=example_decision_maker.decision_options_count,
            decision_options_list=example_decision_maker.decision_options_list,
            evaluation_factors_count=example_decision_maker.evaluation_factors_count,
            evaluation_factors_list=example_decision_maker.evaluation_factors_list,
            evaluation_factor_importance_dict=example_decision_maker.evaluation_factor_importance_dict,
            decision_options_evaluation_dict=example_decision_options_evaluation_dict_w_new_decision_option_evaluation
        )

        decision_maker_old.set_decision_options_evaluation_df(
            example_decision_options_evaluation_df_w_new_decision_option_evaluation)

        assert decision_maker_old == decision_maker_new
