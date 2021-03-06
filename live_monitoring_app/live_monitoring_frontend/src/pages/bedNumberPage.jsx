import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { StyleSheet, Text, View } from "react-native";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faAngleLeft,
  faToilet,
  faAngleDoubleRight,
  faWalking
} from "@fortawesome/free-solid-svg-icons";
import { withRouter } from "react-router-dom";
import axios from "axios";
import NumPad from "react-numpad";
import "../styles/buttons.css"

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

const timeStarted = Date.now();

class bedNumberPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      patientAccompanied: props.location.state.patientAccompanied,
      bedNumber: 0,
      isNotNumeric: 0,
      isNotValidBedNumber: 0,
      timeStarted: timeStarted,
    };
  }

  backPage = () => {
    this.props.history.push("/");
  };

  nextPage = () => {
    this.props.history.push({
      pathname: "/fallriskstatus",
      state: {
        patientAccompanied: this.state.patientAccompanied,
        bedNumber: this.state.bedNumber,
        timeStarted: this.state.timeStarted,
      },
    });
  };

  onBedNumberChange = (value) => {
    this.setState({ bedNumber: value }, () => {});
  };

  postData = () => {
    console.log("post data called") 
    const params = {
      bed_number: this.state.bedNumber, //streamlit
      patient_accompanied: this.state.patientAccompanied, //streamlit
    };

    api.post("/patient-information", params).then((res) => {
      console.log(res.status);
      console.log(res.data.bed_number);
      console.log(res.data);
      if (res.status === 200){
        console.log("Bed number recorded.")
      }
    })
    .catch((err) => {
      console.log("Unable to start toileting session. Please try again.") 
      console.log(err.response);
      console.log(err.request);
    });;
  };

  onSubmitBedNumber = () => {
    if (isNaN(this.state.bedNumber)) {
      this.setState({ isNotNumeric: 1 }, () => {
        this.render();
      });
    } else if (this.state.bedNumber <= 0 || this.state.bedNumber > 40) {
      this.setState({ isNotValidBedNumber: 1 }, () => {
        this.render();
      });
    } else {
      this.postData();
      this.nextPage();
    }
  };

  render() {
    return (
      <View>
        <View style={styles.status}>
          <Text style={styles.textHeaderLight}>Patient is:</Text>
          <Text style={styles.textAccompaniedStatus}>
            {this.state.patientAccompanied ? "Accompanied" : "Alone"}
          </Text>
        </View>

        <View style={styles.bedNumberForm}>
          <Text style={styles.textHeaderDark}>Enter bed number:</Text>

          <NumPad.Number
            onChange={(value) => this.onBedNumberChange(value)}
            negative="False"
            decimal = {0}
            placeholder = "0"
          >
            <button type="button" class="btn btn-outline-dark btn-lg" id="bed-no-bttn">
              {this.state.bedNumber}
            </button>
          </NumPad.Number>

          <Text style={styles.textAlert}>
            {this.state.isNotNumeric
              ? "Invalid input. Please key in a number."
              : null}
          </Text>

          <Text style={styles.textAlert}>
            {this.state.isNotValidBedNumber
              ? "Invalid bed number. Please key in a valid bed number."
              : null}
          </Text>
        </View>

        <View style={styles.divider}></View>

        <View style={styles.buttons}>
          <button
            id="default-bttn"
            type="button"
            className="btn btn-outline-dark"
            onClick={() => this.backPage()}
          >
            <FontAwesomeIcon icon={faAngleLeft} size="2x" />
            <div>back</div>

          </button>

          <button
            id="default-bttn"
            type="button"
            className="btn btn-success"
            onClick={() => this.onSubmitBedNumber()}
          >
            <FontAwesomeIcon icon={faWalking} size="2x" />
            <FontAwesomeIcon icon={faAngleDoubleRight} size="2x" />
            <FontAwesomeIcon icon={faToilet} size="2x" />
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
    backgroundColor: "#353b40",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
  },

  bedNumberForm: {
    flex: 1,
    backgroundColor: "#ffffff",
    alignItems: "center",
    justifyContent: "center",
    padding: "30px",
  },

  buttons: {
    flex: 1,
    flexDirection: "row",
    height: "100px",
    justifyContent: "space-between",
    marginBottom: 36,
    padding: 15,
  },

  textAccompaniedStatus: {
    fontFamily: "Gotham-Ultra",
    fontSize: "60px",
    color: "white",
  },

  textHeaderLight: {
    fontFamily: "Gotham-Black",
    fontSize: "30px",
    color: "white",
  },

  textHeaderDark: {
    fontFamily: "Gotham-Black",
    color: "#566c79",
    fontSize: "40px",
  },

  textAlert: {
    fontFamily: "Gotham-Medium",
    color: "red",
    fontSize: "15px",
  },

  divider: {
    padding: "160px",
  },

  input: {
    borderWidth: 2,
    borderColor: "#566c79",
    padding: 8,
    margin: 10,
    width: 200,
    textAlign: "center",
    fontSize: "40px",
  },
});


