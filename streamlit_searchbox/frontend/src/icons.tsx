import React from "react";

/*
This file contains the icons used in the searchbox component. See https://lucide.dev/icons
*/

// default icon
export const DropdownIcon: React.FC<React.SVGProps<SVGSVGElement>> = (
  props,
) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M12.7071 15.2929L17.1464 10.8536C17.4614 10.5386 17.2383 10 16.7929 10L7.20711 10C6.76165 10 6.53857 10.5386 6.85355 10.8536L11.2929 15.2929C11.6834 15.6834 12.3166 15.6834 12.7071 15.2929Z"></path>
  </svg>
);

// default icon
export const ClearIconCircularFilled: React.FC<
  React.SVGProps<SVGSVGElement>
> = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" {...props}>
    <path
      fill-rule="evenodd"
      clip-rule="evenodd"
      d="M12 20C16.4183 20 20 16.4183 20 12C20 7.58173 16.4183 4 12 4C7.58173 4 4 7.58173 4 12C4 16.4183 7.58173 20 12 20ZM10.0303 8.96967C9.73743 8.67679 9.26257 8.67679 8.96967 8.96967C8.67676 9.26257 8.67676 9.73743 8.96967 10.0303L10.9393 12L8.96967 13.9697C8.67676 14.2626 8.67676 14.7374 8.96967 15.0303C9.26257 15.3232 9.73743 15.3232 10.0303 15.0303L12 13.0607L13.9697 15.0303C14.2626 15.3232 14.7374 15.3232 15.0303 15.0303C15.3232 14.7374 15.3232 14.2626 15.0303 13.9697L13.0607 12L15.0303 10.0303C15.3232 9.73743 15.3232 9.26257 15.0303 8.96967C14.7374 8.67679 14.2626 8.67679 13.9697 8.96967L12 10.9393L10.0303 8.96967Z"
    ></path>
  </svg>
);

// optional icon
export const ClearIconCircularUnfilled: React.FC<
  React.SVGProps<SVGSVGElement>
> = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="3"
    stroke-linecap="round"
    stroke-linejoin="round"
    {...props}
  >
    <circle cx="12" cy="12" r="10" />
    <path d="m15 9-6 6" />
    <path d="m9 9 6 6" />
  </svg>
);

// optional icon
export const ClearIconCross: React.FC<React.SVGProps<SVGSVGElement>> = (
  props,
) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    // default, overwritten by styles
    stroke-width="3"
    stroke-linecap="round"
    stroke-linejoin="round"
    {...props}
  >
    <path d="M18 6 6 18" stroke={props.stroke} />
    <path d="m6 6 12 12" stroke={props.stroke} />
  </svg>
);
