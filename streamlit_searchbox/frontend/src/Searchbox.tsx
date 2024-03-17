import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

import SearchboxStyle from "./styling";
import Select, { InputActionMeta, components } from "react-select";

type Option = {
  value: string;
  label: string;
};

interface State {
  menu: boolean;
  option: Option | null;
  inputValue: string;
}

interface StreamlitReturn {
  interaction: "submit" | "search" | "reset";
  value: any;
}

export function streamlitReturn(interaction: string, value: any): void {
  Streamlit.setComponentValue({
    interaction: interaction,
    value: value,
  } as StreamlitReturn);
}

class Searchbox extends StreamlitComponentBase<State> {
  public state: State = {
    menu: false,
    option: null,
    inputValue: "",
  };

  private style = new SearchboxStyle(this.props.theme!);
  private ref: any = React.createRef();

  /**
   * new keystroke on searchbox
   * @param input
   * @param _
   * @returns
   */
  private callbackSearch = (input: string): void => {
    this.setState({
      inputValue: input,
    });

    streamlitReturn("search", input);
  };

  /**
   * reset button was clicked
   */
  private callbackReset(): void {
    this.setState({
      menu: false,
      option: null,
      inputValue: "",
    });

    streamlitReturn("reset", null);
  }

  /**
   * submitted selection, clear optionally
   * @param option
   */
  private callbackSubmit(option: Option) {
    console.log("callbackSubmit");
    console.log("option", this.state.option, option);

    if (this.props.args.clear_on_submit) {
      this.setState({
        menu: false,
        option: null,
        inputValue: "",
      });
    } else {
      console.log("keep value on submit", this.props.args.input_value);
      console.log("option", option);

      this.setState({
        menu: false,
        // keep value on submit
        option: {
          value: option.value,
          label: option.label,
        },
        inputValue: option.label,
      });
    }

    streamlitReturn("submit", option.value);
  }

  /**
   * show searchbox with label on top
   * @returns
   */
  public render = (): ReactNode => {
    console.log(
      "render",
      this.state.option,
      this.state.inputValue,
      this.props.disabled
    );
    console.log(this.props);

    // TODO: broken

    // https://react-select.com/advanced
    // "Below is an example of replicating the behaviour of the deprecated props from react-select v1, onSelectResetsInput and closeOnSelect"

    // describes the issue with resetting input value
    // https://github.com/JedWatson/react-select/discussions/4302

    return (
      <div>
        {this.props.args.label && (
          <div style={this.style.label}>{this.props.args.label}</div>
        )}

        <Select
          {...{
            onSelectResetsInput: false,
          }}
          name="stateful-select"
          // showing the disabled react-select leads to the component
          // not showing the inputValue but just an empty input field
          // we therefore need to re-render the component if we want to keep the focus
          value={this.state.option}
          inputValue={this.state.inputValue}
          isClearable={true}
          isSearchable={true}
          styles={this.style.select}
          options={this.props.args.options}
          placeholder={this.props.args.placeholder}
          // component overrides
          components={{
            ClearIndicator: (props) => this.style.clearIndicator(props),
            DropdownIndicator: () => this.style.iconDropdown(this.state.menu),
            IndicatorSeparator: () => <div></div>,
          }}
          // handlers
          filterOption={(_, __) => true}
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          onChange={(option: any, a: any) => {
            switch (a.action) {
              case "select-option":
                this.callbackSubmit(option);
                return;

              case "clear":
                this.callbackReset();
                return;
            }
            console.log("onChange", a);
          }}
          onInputChange={(
            inputValue: string,
            { action, prevInputValue }: InputActionMeta
          ) => {
            switch (action) {
              // ignore menu close or blur/unfocus events
              case "input-change":
                this.callbackSearch(inputValue);
                return inputValue;
            }

            console.log("onInputChange", inputValue, action, prevInputValue);
            return prevInputValue;
          }}
          onMenuOpen={() => this.setState({ menu: true })}
          onMenuClose={() => this.setState({ menu: false })}
          menuIsOpen={this.props.args.options && this.state.menu}
        />
      </div>
    );
  };
}
export default withStreamlitConnection(Searchbox);
