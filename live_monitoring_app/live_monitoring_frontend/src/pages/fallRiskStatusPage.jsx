import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { StyleSheet, Text, View } from "react-native";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faAngleLeft,
  faDoorOpen,
  faWalking,
} from "@fortawesome/free-solid-svg-icons";
import { withRouter } from "react-router-dom";
import axios from "axios";
import Sound from "react-sound";

import cautionSign from "../images/warning-256.png";
import fallAlertSound from "../sounds/fall_alert3.mp3";
import comeNowSound from "../sounds/come_now_alert2.mp3";
import getReadySound from "../sounds/get_ready_alert.mp3";
import tamAlertSound from "../sounds/tam_alert.mp3";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

var fallRiskStatus = "low";
var isAbort = true;

class readyPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      patientAccompanied: props.location.state.patientAccompanied,
      bedNumber: props.location.state.bedNumber,
      fallRiskStatus: fallRiskStatus,
      timeStarted: props.location.state.timeStarted,
      timeElapsedMinutes: 0,
      timeElapsedSeconds: "00",
    };
  }

  componentDidMount() {
    this.interval = setInterval(() => {
      var fall_risk_status = this.getFallRiskStatus();

      var newTimeElapsedSeconds = parseInt(this.state.timeElapsedSeconds) + 1;

      if (newTimeElapsedSeconds % 60 === 0) {
        //to increment if it's a new minute
        var newTimeElapsedMinutes = this.state.timeElapsedMinutes + 1;
        newTimeElapsedSeconds = 0;
        this.setState({ timeElapsedMinutes: newTimeElapsedMinutes });
      }

      this.setState({
        fallRiskStatus: fall_risk_status,
        timeElapsedSeconds:
          newTimeElapsedSeconds < 10
            ? "0" + newTimeElapsedSeconds
            : newTimeElapsedSeconds,
      });
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  getFallRiskStatus = () => {
    api
      .get("/patient-information")
      .then((res) => {
        console.log(res.data.fall_risk_status);
        fallRiskStatus = res.data.fall_risk_status;
        return fallRiskStatus;
      })
      .catch((err) => {
        console.log(err.response);
        console.log(err.request);
      });
  };

  deleteData = (isAbort) => {
    api
      .delete("/patient-information", isAbort)
      .then((res) => {
        console.log(res.status);
        console.log(res.data);
        if (res.status == 200) {
          console.log("Toileting session successfully ended.");
        }
      })
      .catch((err) => {
        console.log(err.response);
        console.log(err.request);
      });
  };

  backPage = () => {
    
    this.deleteData(1);
    this.props.history.push({
      pathname: "/bednumber",
      state: { patientAccompanied: this.state.patientAccompanied },
    });
  };

  nextPage = () => {
    this.props.history.push({
      pathname: "/fallriskstatus",
      state: {
        patientAccompanied: this.state.patientAccompanied,
        bedNumber: this.state.bedNumber,
      },
    });
  };

  onEndSession = () => {
    this.props.history.push("/");
    this.deleteData(0);
    console.log("session ended");
  };

  render() {
    var currentStatus;

    if (this.state.fallRiskStatus === "low") {
      currentStatus = (
        <View style={styles.noAction}>
          <Text style={styles.textStatus}>No Action Needed</Text>
        </View>
      );
    } else if (this.state.fallRiskStatus === "mod") {
      currentStatus = (
        <View style={styles.getReady}>
          <Text style={styles.textStatus}>Get Ready</Text>
          <Sound
            url={getReadySound}
            loop="True"
            playStatus={Sound.status.PLAYING}
          />
        </View>
      );
    } else if (this.state.fallRiskStatus === "tam") {
      currentStatus = (
        <View style={styles.tampered}>
          <Text style={styles.textStatus}>Camera is Blocked</Text>
          <Sound
            url={tamAlertSound}
            loop="True"
            playStatus={Sound.status.PLAYING}
          />
        </View>
      );
    } else if (this.state.fallRiskStatus === "fall") {
      currentStatus = (
        <View style={styles.fall}>
          <img src={cautionSign} />
          <Text style={styles.textStatus}>COME NOW</Text>
          <img src={cautionSign} />
          <Sound
            url={fallAlertSound}
            loop="True"
            playStatus={Sound.status.PLAYING}
          />
        </View>
      );
    } else if (this.state.fallRiskStatus === "high") {
      currentStatus = (
        <View style={styles.comeNow}>
          <Text style={styles.textStatus}>COME NOW</Text>
          <Sound
            url={comeNowSound}
            loop="True"
            playStatus={Sound.status.PLAYING}
          />
        </View>
      );
    } else {
      currentStatus = (
        <View style={styles.noAction}>
          <Text style={styles.textStatus}>Patient is Accompanied</Text>
        </View>
      );
    }

    return (
      <View>
        <View style={styles.statusBar}>
          <View>
            <Text style={styles.textHeaderLight}>Patient Status</Text>
            <Text style={styles.textAccompaniedStatus}>
              {this.state.patientAccompanied ? "Accompanied" : "Alone"}
            </Text>
          </View>

          <View>
            <Text style={styles.textHeaderLightCenter}>Time Elapsed</Text>
            <Text style={styles.textTimeElapsed}>
              {this.state.timeElapsedMinutes} : {this.state.timeElapsedSeconds}
            </Text>
          </View>

          <View>
            <Text style={styles.textHeaderLight}>Bed Number</Text>
            <Text style={styles.textBedNumber}>{this.state.bedNumber}</Text>
          </View>
        </View>

        {currentStatus}

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
            className="btn btn-danger"
            onClick={() => this.onEndSession()}
          >
            <FontAwesomeIcon icon={faWalking} size="2x" />
            <FontAwesomeIcon icon={faDoorOpen} size="2x" />
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
    backgroundColor: "#353b40",
    flexDirection: "row",
    // alignItems: 'center',
    justifyContent: "space-between",
    padding: "15px",
  },

  noAction: {
    flex: 1,
    backgroundColor: "#008450",
    alignItems: "center",
    justifyContent: "center",
    paddingBottom: "210px",
    paddingTop: "210px",
    textAlign: "center",
  },

  getReady: {
    flex: 1,
    backgroundColor: "#EFB700",
    alignItems: "center",
    justifyContent: "center",
    paddingBottom: "210px",
    paddingTop: "210px",
  },

  comeNow: {
    flex: 1,
    backgroundColor: "#B81D13",
    alignItems: "center",
    justifyContent: "center",
    padding: "210px",
    flexDirection: "row",
    textAlign: "center",
  },

  fall: {
    flex: 1,
    backgroundColor: "#B81D13",
    alignItems: "center",
    justifyContent: "center",
    padding: "140px",
    flexDirection: "row",
    textAlign: "center",
  },

  tampered: {
    flex: 1,
    backgroundColor: "#000000",
    alignItems: "center",
    justifyContent: "center",
    paddingBottom: "210px",
    paddingTop: "210px",
    textAlign: "center",
  },

  textStatus: {
    fontFamily: "Gotham-Ultra",
    fontSize: "100px",
    color: "white",
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
    alignItems: "center",
    marginBottom: 36,
    padding: 20,
  },

  textAccompaniedStatus: {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white",
  },

  textTimeElapsed: {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white",
    textAlign: "center",
  },

  textBedNumber: {
    fontFamily: "Gotham-Book",
    fontSize: "40px",
    color: "white",
    textAlign: "right",
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
    color: "#566c79",
  },

  textAlert: {
    fontFamily: "Gotham-Medium",
    color: "red",
    fontSize: "15px",
  },

  divider: {
    width: "200px",
  },
});
