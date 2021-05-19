import React, {Component} from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {StyleSheet, Text, TextInput, View} from 'react-native';
import "../styles/buttons.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {faAngleLeft,faToilet,faDoorOpen, faWalking} from "@fortawesome/free-solid-svg-icons";
import { withRouter } from "react-router-dom";


class readyPage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      patientAccompanied: props.location.state.patientAccompanied,
      bedNumber: props.location.state.bedNumber,

      fallRiskStatus: "mod",
      timeElapsed: 1621448932,
    }
  }

  backPage = () => {
    this.props.history.push({ pathname: "/bednumber", state: {patientAccompanied: this.state.patientAccompanied}});
  }

  nextPage = () => {
    this.props.history.push({ pathname: "/fallriskstatus", state: {patientAccompanied: this.state.patientAccompanied, bedNumber: this.state.bedNumber}});
  }

  onEndSession = () => {
    this.props.history.push("/");
    console.log("session ended");
  }

  render () {

    var currentStatus;

    if (this.state.fallRiskStatus == "low"){
      currentStatus = <View style = {styles.noAction}>
      <Text style = {styles.textStatus}>No Action Needed</Text>
      </View>
    } else if (this.state.fallRiskStatus == "mod") {
      currentStatus = <View style = {styles.getReady}>
      <Text style = {styles.textStatus}>Get Ready</Text>
      </View>
    } else { 
      currentStatus = <View style = {styles.comeNow}>
      <Text style = {styles.textStatus}>COME NOW</Text>
      </View>
    }

    return (
      <View>
      <View style = {styles.statusBar}>

        <View>
          <Text style = {styles.textHeaderLight}>Patient is:</Text>
          <Text style = {styles.textAccompaniedStatus}>{this.state.patientAccompanied ? "Accompanied" : "Alone"}</Text>
        </View>

        <View>
          <Text style = {styles.textHeaderLightCenter}>Time elapsed:</Text>
          <Text style = {styles.textTimeElapsed}>{this.state.timeElapsed} mins </Text>
        </View>

        <View>
          <Text style = {styles.textHeaderLight}>Bed number:</Text>
          <Text style = {styles.textBedNumber}>{this.state.bedNumber}</Text>
        </View>
      
      </View>

      {currentStatus}

      <View style = {styles.buttons}>
        <button id="default-bttn" type="button" className="btn btn-outline-dark" onClick={() => this.backPage()}>
          <FontAwesomeIcon icon ={faAngleLeft} size = "2x" />
          <div>back</div>
          </button>

          <button id="default-bttn" type="button" className="btn btn-danger" onClick={() => this.onEndSession()}>
          <FontAwesomeIcon icon ={faWalking} size = "2x" />
          <FontAwesomeIcon icon ={faDoorOpen} size = "2x" />
          <div>end toileting session</div>
          </button>
        
      </View>
    </View>  
    );
  }
  
}

export default withRouter(readyPage);


const styles = StyleSheet.create({
  statusBar: {
    flex: 1,
    backgroundColor: '#353b40',
    flexDirection: "row",
    // alignItems: 'center',
    justifyContent: 'space-between',
    padding: '20px',
  },

  noAction: {
    flex: 1,
    backgroundColor: '#008450',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '210px',
  },

  getReady: {
    flex: 1,
    backgroundColor: '#EFB700',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '210px',
  },

  comeNow: {
    flex: 1,
    backgroundColor: '#B81D13',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '210px',
  },

  textStatus: {
    fontFamily: "Gotham-Ultra",
    fontSize: "100px",
    color: "white"
  }, 

  bedNumberForm: {
    flex: 1,
    backgroundColor: '#ffffff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '30px',
  },

  buttons: {
    flex: 1,
    flexDirection: "row",
    height: "100px",
    justifyContent: "space-between",
    marginBottom: 36,
    padding: 30
  },

  textAccompaniedStatus: {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white"
  },

  textTimeElapsed: {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white",
    textAlign: "center",
  },

  textBedNumber : {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white",
    textAlign: "right"
  },

  textHeaderLight: {
    fontFamily: "Gotham-Black",
    fontSize: "30px",
    color: "white",
},

textHeaderLightCenter: {
  fontFamily: "Gotham-Black",
  fontSize: "30px",
  color: "white",
  textAlign: "center",
},

textHeaderDark: {
    fontFamily: "Gotham-Black",
    fontSize: "20px",
    color: "#566c79"
},


textAlert: {
    fontFamily: "Gotham-Medium",
    color: "red",
    fontSize: "15px"
},

  divider: {
    width: "200px",
  },

});