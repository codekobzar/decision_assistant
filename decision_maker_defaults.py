from decision_maker import DecisionMaker

default_decision = "What is the best way to take decisions?"
default_decision_options_list = [
    "Option 1",
    "Option 2",
    "Option 3",
]
default_evaluation_factors_list = [
    "Factor 1",
    "Factor 2",
]
default_evaluation_factor_importance_dict = {
    factor: DecisionMaker.DEFAULT_EVALUATION_FACTOR_IMPORTANCE
    for factor in default_evaluation_factors_list
}
default_decision_options_evaluation_dict = {
    decision: {
        factor: DecisionMaker.DEFAULT_DECISION_OPTION_VALUE
        for factor in default_evaluation_factors_list
    } for decision in default_decision_options_list
}
default_decision_maker = DecisionMaker()
default_decision_maker.set_attributes(
    decision=default_decision,
    decision_options_count=len(default_decision_options_list),
    decision_options_list=default_decision_options_list,
    evaluation_factors_count=len(default_evaluation_factors_list),
    evaluation_factors_list=default_evaluation_factors_list,
    evaluation_factor_importance_dict=default_evaluation_factor_importance_dict,
    decision_options_evaluation_dict=default_decision_options_evaluation_dict
)
