import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";
import Select from "react-select";

import SearchboxStyle from "./styling";

type Option = {
  value: string;
  label: string;
};

interface State {
  menu: boolean;
  option: Option | null;
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
  public state = {
    menu: false,
    option: null,
  };

  private style = new SearchboxStyle(this.props.theme!);
  private ref: any = React.createRef();

  /**
   * new keystroke on searchbox
   * @param input
   * @param _
   * @returns
   */
  private onSearchInput = (input: string, _: any): void => {
    this.setState({
      option: {
        value: input,
        label: input,
      },
    });

    // happens on selection
    if (input.length === 0) {
      this.setState({ menu: false });
      return;
    }

    streamlitReturn("search", input);
  };

  /**
   * input was selected from dropdown or focus changed
   * @param option
   * @returns
   */
  private onInputSelection(option: Option): void {
    // clear selection (X)
    if (option === null) {
      this.callbackReset();
      return;
    }

    this.callbackSubmit(option);
  }

  /**
   * reset button was clicked
   */
  private callbackReset(): void {
    this.setState({
      menu: false,
      option: null,
    });
    streamlitReturn("reset", null);
  }

  /**
   * submitted selection, clear optionally
   * @param option
   */
  private callbackSubmit(option: Option) {
    streamlitReturn("submit", option.value);

    if (this.props.args.clear_on_submit) {
      this.setState({
        menu: false,
        option: null,
      });
    } else {
      this.setState({
        menu: false,
        option: {
          value: option.value,
          label: option.label,
        },
      });
    }
  }

  /**
   * show searchbox with label on top
   * @returns
   */
  public render = (): ReactNode => {
    return (
      <div>
        {this.props.args.label ? (
          <div style={this.style.label}>{this.props.args.label}</div>
        ) : null}
        <Select
          value={this.state.option}
          inputId={this.props.args.label || "searchbox-input-id"}
          // dereference on clear
          ref={this.ref}
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
          onChange={(e: any) => this.onInputSelection(e)}
          onInputChange={(e, a) => {
            // ignore menu close or blur/unfocus events
            if (a.action === "input-change") this.onSearchInput(e, a);
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
