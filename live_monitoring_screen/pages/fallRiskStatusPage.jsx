import React, {Component} from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, StyleSheet, Text, View } from 'react-native';
import "../styles/buttons.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {faUserNurse, faUser} from "@fortawesome/free-solid-svg-icons";
import { withRouter } from "react-router-dom";

class readyPage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      patientAccompanied: 1
    }
  }

  startSession = (patientAccompaniedBoolean) => {
    this.setState({patientAccompanied: patientAccompaniedBoolean}, () => {
      console.log(this.state.patientAccompanied)
    });

    this.props.history.push("/");
  }

  render () {
    return (
      <View>
        <View style = {styles.ready}>
          <Text style = {styles.textready}>READY</Text>
        </View>
  
        <View style = {styles.letsgetstarted}>
          <Text style = {styles.textbody} >Patient will be ... </Text>
        </View>
  
        <View style = {styles.buttons}>
          <button styles = {styles.buttonText} type="button" className="btn btn-outline-dark" onClick={() => this.startSession(1)}>
            <FontAwesomeIcon icon ={faUserNurse} size = "4x" />
            <FontAwesomeIcon icon ={faUser} size = "4x" />
            <div>ACCOMPANIED</div>
            </button>
          <View style={styles.divider}>
          </View>
          <button styles = {styles.buttonText} type="button" className="btn btn-outline-dark" onClick={() => this.startSession(0)}>
            <FontAwesomeIcon icon ={faUser} size = "4x" />
            <div>ALONE</div>
            </button>
        </View>
      </View>  
    );
  }
  
}

export default withRouter(readyPage);

const styles = StyleSheet.create({
  ready: {
    flex: 1,
    backgroundColor: '#EFB700',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '200px',
  },

  letsgetstarted: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: "20px",
  },

  buttons: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    height: "180px"
  },

  textready: {
      fontFamily: "Gotham-Ultra",
      fontSize: "100px",
      color: "white"
  },

  textbody: {
    fontFamily: "Gotham-Medium",
    color: "black",
    fontSize: "30px"
  },

  divider: {
    width: "200px",
  },

  buttonText: {
    fontFamily: "Gotham-Ultra",
    color: "white",
    padding: 30
  }
});

