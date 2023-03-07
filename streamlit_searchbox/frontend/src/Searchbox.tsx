import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Select from "react-select"

import SearchboxStyle from "./styling"

interface State {
  menu: boolean
}

interface StreamlitReturn {
  interaction: "submit" | "search" | "reset"
  value: any
}

export function streamlitReturn(interaction: string, value: any): void {
  Streamlit.setComponentValue({
    interaction: interaction,
    value: value,
  } as StreamlitReturn)
}

class Searchbox extends StreamlitComponentBase<State> {
  public state = { menu: false }

  private style = new SearchboxStyle(this.props.theme!)
  private ref: any = React.createRef()

  /**
   * new keystroke on searchbox
   * @param input
   * @param _
   * @returns
   */
  private onSearchInput = (input: string, _: any): void => {
    // happens on selection
    if (input.length === 0) {
      this.setState({ menu: false })
      return
    }

    streamlitReturn("search", input)
  }

  /**
   * input was selected from dropdown or focus changed
   * @param option
   * @returns
   */
  private onInputSelection(option: any): void {
    // clear selection (X)
    if (option === null) {
      this.callbackReset()
      return
    }

    this.callbackSubmit(option)
  }

  /**
   * reset button was clicked
   */
  private callbackReset(): void {
    this.setState({
      menu: false,
    })
    streamlitReturn("reset", null)
  }

  /**
   * submitted selection, clear optionally
   * @param option
   */
  private callbackSubmit(option: any) {
    streamlitReturn("submit", option.value)

    if (this.props.args.clear_on_submit) {
      this.ref.current.select.clearValue()
    } else {
      this.setState({
        menu: false,
      })
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
          onChange={(e) => this.onInputSelection(e)}
          onInputChange={(e, a) => this.onSearchInput(e, a)}
          onMenuOpen={() => this.setState({ menu: true })}
          onMenuClose={() => this.setState({ menu: false })}
          menuIsOpen={this.props.args.options && this.state.menu}
        />
      </div>
    )
  }
}
export default withStreamlitConnection(Searchbox)
