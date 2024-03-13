from decision_maker import DecisionMaker

example_decision = "What is the best way to take decisions?"
example_decision_options_list = [
    "Flip a coin",
    "Listen to your heart",
    "Hire a consultant",
    "Use decision maker"
]
example_evaluation_factors_list = [
    "Speed",
    "Quality",
    "Cost",
    "Certainty"
]
example_evaluation_factor_importance_dict = {
    "Speed": 4,
    "Quality": 9,
    "Cost": 2,
    "Certainty": 6
}
example_decision_options_evaluation_dict = {
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
example_decision_maker = DecisionMaker()
example_decision_maker.set_attributes(
    decision=example_decision,
    decision_options_count=len(example_decision_options_list),
    decision_options_list=example_decision_options_list,
    evaluation_factors_count=len(example_evaluation_factors_list),
    evaluation_factors_list=example_evaluation_factors_list,
    evaluation_factor_importance_dict=example_evaluation_factor_importance_dict,
    decision_options_evaluation_dict=example_decision_options_evaluation_dict
)
