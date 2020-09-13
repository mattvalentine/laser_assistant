<template>
  <div id="app" class="ui">
    <DesignSVG v-if="svgLoaded" :designsvg="designModel" />
    <OutputSVG v-if="svgLoaded" :outsvg="outputModel" />
    <EdgeSVG
      v-if="svgLoaded"
      v-on:edgeClick="edgeClick"
      :edge_data="inputModel.edge_data"
      :joints="inputModel.joints"
    />
    <Parameters
      v-if="svgLoaded"
      v-on:update="updateParams"
      :thickness="laserParams.thickness"
      :kerf="laserParams.kerf"
      :material="laserParams.material"
      :scaleFactor="laserParams.scaleFactor"
      @download="downloadsvg"
    />
    <LoadSVG v-if="!svgLoaded" v-on:insvg="loadSVG" />
    <JointParams
      v-show="showJointParams"
      @confirm="confirmEdge"
      :setjp="setjp"
      @flipjoint="flipjoint"
    />
  </div>
</template>

<script>
import DesignSVG from "./components/DesignSVG";
import OutputSVG from "./components/OutputSVG";
import EdgeSVG from "./components/EdgeSVG";
import Parameters from "./components/Parameters";
import LoadSVG from "./components/LoadSVG";
import JointParams from "./components/JointParams";
const axios = require("axios").default;

export default {
  name: "App",
  components: {
    DesignSVG,
    OutputSVG,
    EdgeSVG,
    Parameters,
    LoadSVG,
    JointParams,
  },
  data: function () {
    return {
      svgLoaded: false,
      showJointParams: false,
      outputModel: "<svg/>",
      designModel: "<svg/>",
      inputModel: {
        edge_data: {
          viewBox: "0 0 0 0",
        },
        joint_index: 1,
        joints: {},
      },
      laserParams: {
        thickness: 3.0,
        kerf: 0.05,
        material: "Wood",
        scaleFactor: 1.0,
      },
      AB: true,
      active_joint_name: "Joint0",
      active_joint: {
        edge_a: {},
        edge_b: {},
        joint_parameters: {},
      },
      setjp: {
        joint_type: "Box",
        fit: "Clearance",
        tabsize: 10.0,
        tabspace: 20.0,
        tabnum: 2,
        boltsize: "M2.5",
        boltspace: 20.0,
        boltnum: 2,
        boltlength: 10.0,
      },
      // joint_index: 1,
    };
  },
  methods: {
    loadSVG: function (svgInput) {
      this.svgLoaded = true;
      let formData = new FormData();
      formData.append("svgInput", svgInput);

      axios
        .post("http://127.0.0.1:5000/get_model", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.inputModel = response.data;
          this.updateOutput();
        });
    },
    updateOutput: function () {
      let formData = new FormData();
      formData.append("inputModel", JSON.stringify(this.inputModel));
      formData.append("laserParams", JSON.stringify(this.laserParams));
      axios
        .post("http://127.0.0.1:5000/get_design", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.designModel = response.data;
        });
      axios
        .post("http://127.0.0.1:5000/get_output", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.outputModel = response.data;
        });
    },
    updateParams: function (newParams) {
      console.log(newParams);
      this.laserParams = newParams;
      this.updateOutput();
    },
    isJoint: function (edge) {
      console.log("edge joint check", edge);
      const joints = this.inputModel.joints;
      for (const joint in joints) {
        if (
          joints[joint].edge_a.d === edge.d ||
          joints[joint].edge_b.d === edge.d
        ) {
          return joint;
        }
      }
      return false;
    },
    modifyJoint: function (joint) {
      const joints = this.inputModel.joints;
      this.active_joint_name = joint;
      this.active_joint = joints[joint];
      this.setjp = joints[joint].joint_parameters;
      const edgeelementa = document.getElementById(
        "edge" + this.active_joint.edge_a.edge
      );
      const edgeelementb = document.getElementById(
        "edge" + this.active_joint.edge_b.edge
      );
      edgeelementa.className.baseVal = "edges activeedge";
      edgeelementb.className.baseVal = "edges activeedge";
      this.showJointParams = true;
    },
    flipjoint: function () {
      const oldedgea = this.active_joint.edge_a;
      const oldedgeb = this.active_joint.edge_b;
      this.active_joint.edge_a = oldedgeb;
      this.active_joint.edge_b = oldedgea;
    },
    edgeClick: function (edge) {
      const edgeelement = document.getElementById("edge" + edge.edge);
      const joint = this.isJoint(Object.assign({}, edge));
      if (joint) {
        console.log("foundit");
        this.modifyJoint(joint);
        return;
      }

      edgeelement.className.baseVal = "edges activeedge";
      if (!this.showJointParams) {
        if (this.AB) {
          this.active_joint_name = "Joint" + this.inputModel.joint_index;
          this.active_joint.edge_a = Object.assign({}, edge);
          // console.log(this.active_joint);
        } else {
          this.active_joint.edge_b = Object.assign({}, edge);
          this.showJointParams = true;
          // console.log(this.active_joint);
        }
      }
      this.AB = !this.AB;
    },
    confirmEdge: function (jparams) {
      console.log(jparams);
      this.active_joint.joint_parameters = Object.assign({}, jparams);
      this.inputModel.joints[this.active_joint_name] = Object.assign(
        {},
        this.active_joint
      );

      const edgeelementa = document.getElementById(
        "edge" + this.active_joint.edge_a.edge
      );
      const edgeelementb = document.getElementById(
        "edge" + this.active_joint.edge_b.edge
      );
      edgeelementa.className.baseVal = "edges joint";
      edgeelementb.className.baseVal = "edges joint";
      this.showJointParams = false;
      this.inputModel.joint_index++;
      this.updateOutput();
    },
    downloadsvg: function () {
      const link = document.createElement("a");
      const outsvg = document.getElementById("outputsvg").childNodes[0];
      const svgblob = new Blob([outsvg.outerHTML], { type: "image/svg+xml" });

      link.download = "output.svg";
      link.href = URL.createObjectURL(svgblob);
      link.click();
    },
  },
};
</script>

<style>
body {
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* height: 100vh; */
  width: 100vw;
  font-family: sans-serif;
}

.ui {
  width: 100%;
  display: grid;
  grid-template: "svg panel" 1fr / 3fr 1fr;
  grid-column-gap: 1vw;
  /* width: vmin; */
}

.model {
  grid-area: svg;
  display: grid;
  align-items: center;
  width: 100%;
}
</style>
