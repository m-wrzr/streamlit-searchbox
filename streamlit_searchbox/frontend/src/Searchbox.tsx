import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Select from "react-select"

import { getStyleConfig } from "./styling"

interface State {
  menu: boolean
}

interface StreamlitReturn {
  interaction: "submit" | "search" | "reset"
  value: any
}

class Searchbox extends StreamlitComponentBase<State> {
  public state = { menu: false }

  selectRef: any = null

  clearValue = () => {
    console.log("clearREF")
    this.selectRef.select.clearValue()
  }

  private updateStreamlit = (result: StreamlitReturn): void => {
    Streamlit.setComponentValue(result)
  }

  // new keystroke on searchbox
  private onSearchInput = (input: string, _: any): void => {
    // happens on selection
    if (input.length === 0) {
      this.setState({ menu: false })
      return
    }

    // this.setState({ menu: true })

    this.updateStreamlit({
      interaction: "search",
      value: input,
    } as StreamlitReturn)
  }

  // input was selected from dropdown or focus changed
  private onInputSelection = (option: any): void => {
    // clear selection (X)
    if (option === null) {
      this.setState({
        menu: false,
      })

      this.updateStreamlit({
        interaction: "reset",
        value: null,
      } as StreamlitReturn)

      return
    }

    this.updateStreamlit({
      interaction: "submit",
      value: option.value,
    } as StreamlitReturn)

    if (this.props.args.clear_on_submit) {
      // TODO: null error
      this.clearValue()
    } else {
      this.setState({
        menu: false,
      })
    }
  }

  /**
   *
   * @returns
   */
  public render = (): ReactNode => {
    return (
      <Select
        // dereference on clear
        ref={(ref) => {
          this.selectRef = ref
        }}
        // defaults
        styles={getStyleConfig(this.props.theme!)}
        placeholder={this.props.args.placeholder}
        isSearchable={true}
        isClearable={this.props.args.clearable}
        // handlers
        onInputChange={(e, a) => this.onSearchInput(e, a)}
        onChange={(e) => this.onInputSelection(e)}
        // OPTIONS
        options={this.props.args.options}
        filterOption={(_, __) => true}
        // MENU
        onMenuOpen={() => this.setState({ menu: true })}
        onMenuClose={() => this.setState({ menu: false })}
        menuIsOpen={this.props.args.options && this.state.menu}
      />
    )
  }
}
export default withStreamlitConnection(Searchbox)
