import React from "react";
import {
  Header,
  LeftOptions,
  RightOptions,
  LinkStyled,
} from "./navigation.styles";

const Navigation = () => {
    return (
      <Header>
        <LeftOptions>
          <LinkStyled to="/">Main</LinkStyled>
          <LinkStyled to="/inventory">Products</LinkStyled>
          <LinkStyled to="/deliver">Shipments</LinkStyled>
          <LinkStyled to="/log">Views</LinkStyled>
        </LeftOptions>
        <RightOptions>
        </RightOptions>
      </Header>
    );
  };
  
  export default Navigation;