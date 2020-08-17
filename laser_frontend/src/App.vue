<template>
  <div id="app" class="ui">
    <OutputSVG v-if="svgLoaded" :outsvg="outputModel" />
    <EdgeSVG v-if="svgLoaded" v-on:edgeClick="edgeClick" :edge_data="inputModel.edge_data" />
    <Parameters
      v-if="svgLoaded"
      v-on:update="updateParams"
      :thickness="laserParams.thickness"
      :kerf="laserParams.kerf"
      @download="downloadsvg"
    />
    <LoadSVG v-if="!svgLoaded" v-on:insvg="loadSVG" />
    <JointParams v-if="showJointParams" @confirm="confirmEdge" />
  </div>
</template>

<script>
import OutputSVG from "./components/OutputSVG";
import EdgeSVG from "./components/EdgeSVG";
import Parameters from "./components/Parameters";
import LoadSVG from "./components/LoadSVG";
import JointParams from "./components/JointParams";
const axios = require("axios").default;

export default {
  name: "App",
  components: {
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
      inputModel: {
        edge_data: {
          viewBox: "0 0 0 0",
        },
      },
      laserParams: {
        thickness: 3.1,
        kerf: 0.27,
      },
      AB: true,
      active_joint: {
        a: { name: "JA0", edge: {}, id: "" },
        b: { name: "JB0", edge: {}, id: "" },
      },
      joint_index: 1,
    };
  },
  methods: {
    loadSVG: function (svgInput) {
      this.svgLoaded = true;
      let formData = new FormData();
      formData.append("svgInput", svgInput);
      // formData.append("laserParams", JSON.stringify(this.laserParams));

      axios
        .post("http://127.0.0.1:5000/get_model", formData, {
          // .post("get_model", formData, {
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
      // this.outputModel = outsvg;
      axios
        .post("http://127.0.0.1:5000/get_output", formData, {
          // .post("get_output", formData, {
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
    edgeClick: function (edge) {
      const edgeelement = document.getElementById("edge" + edge.edge);
      // console.log(edge);
      // console.log(edgeelement);
      edgeelement.className.baseVal = "edges activeedge";
      if (!this.showJointParams) {
        if (this.AB) {
          this.active_joint.a.name = "J" + this.joint_index + "A";
          this.active_joint.a.edge = edge;
          this.active_joint.a.id = edgeelement;
        } else {
          this.active_joint.b.name = "J" + this.joint_index + "B";
          this.active_joint.b.edge = edge;
          this.active_joint.b.id = edgeelement;
          this.showJointParams = true;
        }
      }
      this.AB = !this.AB;
    },
    confirmEdge: function (jparams) {
      const edgea = this.active_joint.a;
      const edgeb = this.active_joint.b;

      console.log(jparams);

      this.showJointParams = false;
      this.joint_index++;
      this.inputModel.joints[edgea.name] = {
        path: edgea.edge.d,
        face: edgea.edge.face,
      };
      this.inputModel.joints[edgeb.name] = {
        path: edgeb.edge.d,
        face: edgeb.edge.face,
      };
      edgea.id.className.baseVal = "edges";
      edgeb.id.className.baseVal = "edges";
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
  height: 100vh;
  width: 100vw;
}

.ui {
  width: 100%;
  /* height: 100%; */
  display: grid;
  grid-template: "svg panel" 1fr / 3fr 1fr;
  grid-column-gap: 1vw;
  width: vmin;
}

.model {
  grid-area: svg;
  display: grid;
  align-items: center;
  /* z-index: 0; */
  width: 100%;
}
</style>
