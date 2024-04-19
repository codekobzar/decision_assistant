import pandas as pd
import plotly.express as px
import streamlit as st

from matplotlib.colors import LinearSegmentedColormap

from decision_maker import DecisionMaker
from decision_maker_defaults import default_decision_maker
from decision_maker_mockup import example_decision_maker
from progress_tracker import ProgressTracker
from utils import snake_case, parse_toml

pd.options.plotting.backend = "plotly"
streamlit_config = parse_toml(".streamlit/config.toml")
cmap = LinearSegmentedColormap.from_list(
    "bggradient", [streamlit_config['theme']['backgroundColor'], streamlit_config['theme']['primaryColor']])
plotly_cmap = px.colors.sequential.Tealgrn  # https://plotly.com/python/builtin-colorscales/

def update_session_state_from_decision_maker(decision_maker: DecisionMaker):
    st.session_state['decision_options_count'] = decision_maker.decision_options_count
    for decision_option_number in range(st.session_state['decision_options_count']):
        st.session_state[f'option_{decision_option_number}'] = decision_maker.decision_options_list[
            decision_option_number]
    st.session_state['evaluation_factors_count'] = decision_maker.evaluation_factors_count
    for evaluation_factor_number in range(st.session_state['evaluation_factors_count']):
        st.session_state[f'factor_{evaluation_factor_number}'] = decision_maker.evaluation_factors_list[
            evaluation_factor_number]
        st.session_state[f'factor_{evaluation_factor_number}_importance'] = \
            decision_maker.evaluation_factor_importance_dict[
                decision_maker.evaluation_factors_list[evaluation_factor_number]]
        for decision_option_number in range(st.session_state['decision_options_count']):
            st.session_state[
                f"option_{decision_option_number}_factor_{evaluation_factor_number}"
            ] = decision_maker.decision_options_evaluation_dict[
                decision_maker.decision_options_list[decision_option_number]
            ][
                decision_maker.evaluation_factors_list[evaluation_factor_number]
            ]


def reset_data_editors():
    st.session_state.data_editor_version += 1


def save_changes():
    if not edited_decision_options_df.equals(decision_options_df):
        decision_maker.set_decision_options_with_list(
            edited_decision_options_df["Decision option"].tolist()
        )
        edited_decision_options_evaluation_df.columns = edited_decision_options_df["Decision option"].tolist()
    if not edited_evaluation_factors_df.equals(evaluation_factors_df):
        decision_maker.set_evaluation_factors_with_list(
            edited_evaluation_factors_df["Evaluation factor"].tolist()
        )
        edited_decision_options_evaluation_df.index = edited_evaluation_factors_df["Evaluation factor"].tolist()
        edited_evaluation_factor_importance_df.index = edited_evaluation_factors_df["Evaluation factor"].tolist()
    if not edited_decision_options_evaluation_df.equals(decision_maker.decision_options_evaluation_df):
        decision_maker.set_decision_options_evaluation_df(edited_decision_options_evaluation_df)
    if not edited_evaluation_factor_importance_df.equals(decision_maker.evaluation_factor_importance_df):
        decision_maker.set_evaluation_factor_importance_df(edited_evaluation_factor_importance_df)
    update_session_state_from_decision_maker(decision_maker)


def expander(section_label: str):
    label_in_snake_case = snake_case(section_label)
    return st.expander(
        section_label,
        expanded=st.session_state.progress_tracker.check(label_in_snake_case),
    )


def next_button(section_label: str):
    label_in_snake_case = snake_case(section_label)
    return st.button(
        "Next",
        type='primary',
        key=f"{label_in_snake_case}_next_button",
        on_click=next_section,
        args=[section_label],
    )


def back_button(section_label: str):
    label_in_snake_case = snake_case(section_label)
    return st.button(
        "Back",
        key=f"{label_in_snake_case}_back_button",
        on_click=previous_section,
        args=[section_label],
    )


def next_and_back_buttons(section_label: str):
    col1, col2 = st.columns([1, 14])

    with col1:
        back_button(section_label)
    with col2:
        next_button(section_label)

    return col1, col2


def next_section(section: str):
    progress_tracker.steps_set_active([s for s in progress_tracker.steps if s != snake_case(section)], False)
    progress_tracker.step_set_active(snake_case(section))
    progress_tracker.next()


def previous_section(section: str):
    progress_tracker.steps_set_active([s for s in progress_tracker.steps if s != snake_case(section)], False)
    progress_tracker.step_set_active(snake_case(section))
    progress_tracker.back()


def navigate_to_section(section_label: str):
    progress_tracker.focus(snake_case(section_label))


def fold_all_sections(fold: bool = True):
    progress_tracker.steps_set_active(progress_tracker.steps, not fold)

###########################
### Configuration Setup ###
###########################

st.set_page_config(
    page_title="Decision Maker",
    page_icon=":brain:", layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

section_labels = [
    'Decision',
    'Decision options',
    'Evaluation factors',
    'Evaluation factor importance',
    'Decision options evaluation',
    'Table editor',
    'Final decision inputs',
    'Decision scores',
    'Decision analysis',
]
section_index = 0

if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
debug_mode = st.session_state.debug_mode

# debug_mode = st.toggle("Enable debug mode")

if 'decision_maker' in st.session_state:
    decision_maker = st.session_state['decision_maker']
    if debug_mode:
        st.write("*Using pre-loaded decision maker object.*")
else:
    decision_maker = DecisionMaker()
    decision_maker.set_attributes_from(default_decision_maker)
    st.session_state['decision_maker'] = decision_maker
    if debug_mode:
        st.write("*Using default decision maker object.*")
    update_session_state_from_decision_maker(decision_maker)

if 'progress_tracker' in st.session_state:
    progress_tracker = st.session_state['progress_tracker']
    if debug_mode:
        st.write("*Using pre-loaded progress tracker object.*")
else:
    progress_tracker = ProgressTracker(steps=[snake_case(s) for s in section_labels])
    st.session_state['progress_tracker'] = progress_tracker
    if debug_mode:
        st.write("*Using default progress tracker object.*")

if 'data_editor_version' not in st.session_state:
    st.session_state.data_editor_version = 0

############################
### Production Front End ###
############################

st.title("Welcome to Decision Assistant!")
st.write("This app helps you make decisions by understanding your values, "
         "their importance and how each option aligns with those.")

# Debug mode section
if debug_mode:

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("Use default values"):
            decision_maker.set_attributes_from(default_decision_maker)
            update_session_state_from_decision_maker(decision_maker)
    with col2:
        if st.button("Use mockup values"):
            decision_maker.set_attributes_from(example_decision_maker)
            update_session_state_from_decision_maker(decision_maker)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("Decision maker representation:")
        st.json(decision_maker.to_dict(), expanded=False)
    with col2:
        st.write("Progress tracker representation:")
        st.json(progress_tracker.to_dict(), expanded=False)

# Sidebar
with st.sidebar:
    with st.expander("Quick navigation"):
        if st.button("Fold all sections", key='fold_all_sections_button'):
            fold_all_sections(True)
        st.write('---')
        for section in section_labels:
            st.button(section, on_click=navigate_to_section, args=[section])
        st.write('---')
        if st.button("Unfold all sections", key='unfold_all_sections_button'):
            fold_all_sections(False)

    with st.expander("Decision data download"):
        st.download_button(
            "Download decision data",
            decision_maker.to_csv(),
            "decision_assistant_data.csv",
            "text/csv",
            key='download_decision_data'
        )

    with st.expander("Decision data upload"):
        decision_data_file = st.file_uploader(
            "Upload decision data",
            type=["csv"],
            key="upload_decision_data"
        )
        if decision_data_file:
            decision_data = pd.read_csv(decision_data_file, index_col=0)
            st.write("Data preview")
            st.dataframe(decision_data)
            if st.button("Update decision data"):
                error_message = DecisionMaker.validate_decision_dataframe(decision_data)
                if error_message:
                    st.error(error_message)
                else:
                    decision_maker.from_dataframe(decision_data)
                    update_session_state_from_decision_maker(decision_maker)
                    st.success("Decision data successully updated.")
        else:
            st.write("No data uploaded")

# Main section
st.header("Decision inputs")
with expander(section_labels[0]):
    decision_maker.set_decision(
        st.text_input("What decision do you need to make?",
                      "What is the best way to take decisions?")
    )
    next_button(section_labels[0])

with expander(section_labels[1]):
    decision_maker.set_decision_options_count(
        st.number_input("How many options do you have?",
                        key="decision_options_count", min_value=2)
    )
    for i in range(decision_maker.decision_options_count):
        decision_maker.set_decision_option(
            i,
            st.text_input(
                f"Option {i + 1}",
                value=decision_maker.decision_options_list[i],
                key=f"option_{i}"
            )
        )
    next_and_back_buttons(section_labels[1])

with expander(section_labels[2]):
    st.write("To evaluate each option, we need to understand the evaluation factors of the best decision.")
    decision_maker.set_evaluation_factors_count(
        st.number_input("How many evaluation factors are important?",
                        key="evaluation_factors_count", min_value=1)
    )
    for i in range(decision_maker.evaluation_factors_count):
        decision_maker.set_evaluation_factor(
            i,
            st.text_input(
                f"Factor {i + 1}",
                decision_maker.evaluation_factors_list[i],
                key=f"factor_{i}"
            )
        )
    next_and_back_buttons(section_labels[2])

with expander(section_labels[3]):
    st.write("Rate importance of each evaluation factor with a number from 0 to 10 "
             "where 0 is the least important and 10 is the most important.")
    for i in range(decision_maker.evaluation_factors_count):
        evaluation_factor = decision_maker.evaluation_factors_list[i]
        decision_maker.set_evaluation_factor_importance(
            i,
            st.number_input(
                f"Importance of {evaluation_factor}",
                key=f"factor_{i}_importance",
                value=DecisionMaker.DEFAULT_EVALUATION_FACTOR_IMPORTANCE,
                min_value=DecisionMaker.MIN_EVALUATION_FACTOR_IMPORTANCE,
                max_value=DecisionMaker.MAX_EVALUATION_FACTOR_IMPORTANCE,
            )
        )
    next_and_back_buttons(section_labels[3])

with expander(section_labels[4]):
    st.write("Rate each evaluation factor for each decision option with a number from 0 to 10 "
             "where 0 is the least favorable and 10 is the most favorable.")
    col1, col2 = st.columns([1, 3])
    for evaluation_factor_number in range(decision_maker.evaluation_factors_count):
        evaluation_factor = decision_maker.evaluation_factors_list[evaluation_factor_number]
        for decision_option_number, col in zip(
                range(decision_maker.decision_options_count),
                st.columns(decision_maker.decision_options_count)
        ):
            decision_option = decision_maker.decision_options_list[decision_option_number]
            with col:
                decision_maker.set_decision_options_evaluation(
                    decision_option_number, evaluation_factor_number,
                    st.number_input(
                        f"{evaluation_factor} of {decision_option}",
                        key=f"option_{decision_option_number}"
                            f"_factor_{evaluation_factor_number}",
                        value=DecisionMaker.DEFAULT_DECISION_OPTION_VALUE,
                        min_value=DecisionMaker.MIN_DECISION_OPTION_VALUE,
                        max_value=DecisionMaker.MAX_DECISION_OPTION_VALUE,
                    )
                )
    next_and_back_buttons(section_labels[4])

with expander(section_labels[5]):
    st.write("You can quickly edit the inputs in the tabular format here.")
    col1, col2 = st.columns([1, 5])

    with col1:
        st.write("Decision options:")
        decision_options_df = pd.DataFrame(decision_maker.decision_options_list, columns=["Decision option"])
        edited_decision_options_df = st.data_editor(
            decision_options_df,
            key=f"decision_options_de_{st.session_state.data_editor_version}",
            hide_index=True
        )

    with col2:
        st.write("Decision option values:")
        edited_decision_options_evaluation_df = st.data_editor(
            decision_maker.decision_options_evaluation_df.T,
            key=f"decision_options_evaluation_de_{st.session_state.data_editor_version}",
            hide_index=True
        ).T

    col1, col2 = st.columns([1, 5])

    with col1:
        st.write("Evaluation factors:")
        evaluation_factors_df = pd.DataFrame(decision_maker.evaluation_factors_list, columns=["Evaluation factor"])
        edited_evaluation_factors_df = st.data_editor(
            evaluation_factors_df,
            key=f"evaluation_factors_de_{st.session_state.data_editor_version}",
            hide_index=True
        )

    with col2:
        st.write("Evaluation factor importance:")
        edited_evaluation_factor_importance_df = st.data_editor(
            decision_maker.evaluation_factor_importance_df,
            key=f"evaluation_factor_importance_de_{st.session_state.data_editor_version}",
            hide_index=True
        )

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Revert changes"):
            reset_data_editors()
            st.rerun()

    with col2:
        if st.button("Save changes", on_click=save_changes):
            st.rerun()
    next_and_back_buttons(section_labels[5])

with expander(section_labels[6]):
    st.write("This is the final input the decision scores will be calculated on.")

    col1, col2 = st.columns([1, 5])

    with col1:
        st.write("Evaluation factor importance:")
        st.dataframe(decision_maker.evaluation_factor_importance_df)

    with col2:
        st.write("Decision option values:")
        st.dataframe(decision_maker.decision_options_evaluation_df)
    next_and_back_buttons(section_labels[6])

st.header("Decision outputs")

with expander(section_labels[7]):
    decision_maker.compute_decision_options_evaluation_adj_by_importance_df()
    decision_maker.compute_decision_score()

    st.plotly_chart(
        decision_maker.plot_score(),
        use_container_width=True,
        color_discrete_sequence=plotly_cmap,
    )
    next_and_back_buttons(section_labels[7])

with expander(section_labels[8]):
    st.subheader("Importance factor values by decision option")

    tab1, tab2 = st.tabs([
        "Table",
        "Chart"
    ])

    with tab1:
        st.dataframe(
            decision_maker.style_decision_options_evaluation_df(cmap=cmap)
        )

    with tab2:
        st.plotly_chart(
            decision_maker.plot_decision_options_evaluation_df(),
            use_container_width=True,
            color_discrete_sequence=plotly_cmap,
        )

    st.subheader("Decision score drill-down by importance factor contribution")

    tab1, tab2 = st.tabs([
        "Table",
        "Chart"
    ])

    with tab1:
        st.dataframe(
            decision_maker.style_decision_options_evaluation_adj_by_importance_df(cmap=cmap)
        )

    with tab2:
        st.plotly_chart(
            decision_maker.plot_decision_options_evaluation_adj_by_importance_df(),
            use_container_width=True,
            color_discrete_sequence=plotly_cmap,
        )
    back_button(section_labels[8])

    st.session_state['decision_maker'] = decision_maker
