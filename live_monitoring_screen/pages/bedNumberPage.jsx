import React, {Component} from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {StyleSheet, Text, TextInput, View} from 'react-native';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {faAngleLeft,faToilet,faAngleDoubleRight, faWalking} from "@fortawesome/free-solid-svg-icons";
import { withRouter } from "react-router-dom";
import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:3000/current_patient_details"
  })

const timeStarted = Date.now()

class bedNumberPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      patientAccompanied: props.location.state.patientAccompanied,
      bedNumber: 0,
      isNotNumeric: 0,
      isNotValidBedNumber: 0,
      timeStarted: timeStarted
    };
  }


  backPage = () => {
    this.props.history.push("/");
  }

  nextPage = () => {
    this.props.history.push({ pathname: "/fallriskstatus", state: {patientAccompanied: this.state.patientAccompanied, bedNumber: this.state.bedNumber, timeStarted: this.state.timeStarted}});
  }

  onBedNumberChange = (value) => {
     
      this.setState({bedNumber: value}, () => {
      });

  }

  getData = () => {
    api.get('/').then(res => {
    console.log(res.data[0])
    const data = res.data[0]

   })
  }


  postData = () => {

    const params = { 
        bed_number: this.state.bedNumber,
        patient_accompanied: this.state.patientAccompanied,
        time_started: this.state.timeStarted,
        time_stopped: 0,
        fallRiskStatus: "low"
      }

      api.post("/", params)
      .then((res) => {
          console.log(res.status);
      })
  }


  onSubmitBedNumber = () => {

    if (isNaN(this.state.bedNumber)){
        this.setState({isNotNumeric: 1} , () => {
            this.render()
        })

    } else if ((this.state.bedNumber <= 0) || (this.state.bedNumber > 40)) {
        this.setState({isNotValidBedNumber: 1} , () => {
            this.render()
        })

    } else {
        this.postData();
        this.nextPage();
    }

  }

  render () {
    return (
      <View>
        <View style = {styles.status}>
         <Text style = {styles.textHeaderLight}>Patient is:</Text>
          <Text style = {styles.textAccompaniedStatus}>{this.state.patientAccompanied ? "Accompanied" : "Alone"}</Text>
        </View>

        <View style = {styles.bedNumberForm}>
            <Text style = {styles.textHeaderDark}>Enter bed number:</Text>
             <TextInput 
                style = {styles.input}
                placeholder = "enter bed number"
                onChangeText = {(value) => this.onBedNumberChange(value)}
                keyboardType = "number-pad"
                />

            <Text style = {styles.textAlert}>{this.state.isNotNumeric ? "Invalid input. Please key in a number." : null}</Text>   

            <Text style = {styles.textAlert}>{this.state.isNotValidBedNumber ? "Invalid bed number. Please key in a valid bed number." : null}</Text>   

        </View>

        <View style = {styles.divider}></View>

        {/* <div style = {styles.divider}></div> */}

        <View style = {styles.buttons}>
          <button id="default-bttn" type="button" className="btn btn-outline-dark" onClick={() => this.backPage()}>
            <FontAwesomeIcon icon ={faAngleLeft} size = "2x" />
            <div>back</div>
            </button>

            <button id="default-bttn" type="button" className="btn btn-success" onClick={() => this.onSubmitBedNumber()}>
            <FontAwesomeIcon icon ={faWalking} size = "2x" />
            <FontAwesomeIcon icon ={faAngleDoubleRight} size = "2x" />
            <FontAwesomeIcon icon ={faToilet} size = "2x" />
            <div>start toileting session</div>
            </button>
        </View>
      </View>  
    );
  }
  
}

export default withRouter(bedNumberPage);



const styles = StyleSheet.create({
  status: {
    flex: 1,
    backgroundColor: '#353b40',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
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
      fontFamily: "Gotham-Ultra",
      fontSize: "60px",
      color: "white"
  },

  textHeaderLight: {
    fontFamily: "Gotham-Black",
    fontSize: "30px",
    color: "white"
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
    padding: "180px",
  },

  input : {
    borderWidth: 2, 
    borderColor: "#566c79",
    padding: 8,
    margin: 10,
    width: 200,
    textAlign: "center"
  }

});
