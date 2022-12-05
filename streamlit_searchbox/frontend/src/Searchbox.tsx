import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Select from "react-select"

import { getStyleConfig, getStyledIcon } from "./styling"

interface State {
  search: string
  option: any
  focus: boolean
}

class Searchbox extends StreamlitComponentBase<State> {
  public state = { search: "", option: null, focus: false }

  // new keystroke on searchbox
  private onSearchInput = (input: string, _: any): void => {
    if (input.length > 0) {
      this.setState({ search: input, option: null, focus: true }, () =>
        Streamlit.setComponentValue(this.state)
      )
    }
  }

  // input was selected from dropdown
  private onInputSelection = (option: any): void => {
    this.setState(
      {
        search: "",
        focus: false,
        option: option.value,
      },
      () => Streamlit.setComponentValue(this.state)
    )
  }

  /**
   *
   * @returns
   */
  public render = (): ReactNode => {
    let isSearchActive = this.state.search !== ""

    // always available, no typehint as missing relevant props
    const streamlitTheme: any = this.props.theme!

    return (
      <Select
        styles={getStyleConfig(this.props.theme!)}
        components={{
          DropdownIndicator: () => getStyledIcon(this.props.theme!),
        }}
        placeholder={"Search ..."}
        onInputChange={(e, a) => this.onSearchInput(e, a)}
        onChange={(e) => this.onInputSelection(e)}
        isSearchable={true}
        // show all options, filtering should be done in python
        filterOption={(_, __) => true}
        // always show dropdown
        menuIsOpen={isSearchActive && this.state.focus}
        options={isSearchActive ? this.props.args["options"] : []}
        onFocus={() => this.setState({ focus: true })}
        onBlur={() => this.setState({ focus: false })}
      />
    )
  }
}

export default withStreamlitConnection(Searchbox)
