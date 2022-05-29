import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Select from "react-select"

import { default as SearchIconSvg } from "./magnifying-glass-solid.svg"

interface State {
  search: string
  option: string
}

const SearchIcon = (
  <img
    width={24}
    src={SearchIconSvg}
    alt="Search Icon"
    title="Search Icon"
    style={{ marginLeft: "6px", marginRight: "6px", padding: "4px" }}
  />
)

class Searchbox extends StreamlitComponentBase<State> {
  public state = { search: "", option: "" }

  // new keystroke on searchbox
  private onSearchInput = (input: string, _: any): void => {
    if (input.length > 0) {
      this.setState({ search: input, option: "" }, () =>
        Streamlit.setComponentValue(this.state)
      )
    }
  }

  private onInputSelection = (option: any): void => {
    this.setState(
      {
        search: option.value,
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
    let isSearchActive = this.state.search !== this.state.option

    return (
      <Select
        components={{
          DropdownIndicator: () => SearchIcon,
        }}
        placeholder={"Search ..."}
        onInputChange={(e, a) => this.onSearchInput(e, a)}
        onChange={(e) => this.onInputSelection(e)}
        isSearchable={true}
        // show all options, filtering should be done in python
        filterOption={(_, __) => true}
        // always show dropdown
        menuIsOpen={isSearchActive}
        options={isSearchActive ? this.props.args["options"] : []}
      />
    )
  }
}

export default withStreamlitConnection(Searchbox)
