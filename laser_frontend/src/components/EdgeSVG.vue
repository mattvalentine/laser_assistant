<template>
  <div class="edge-model">
    <svg id="Layer" :viewBox="edge_data.viewBox" xmlns="http://www.w3.org/2000/svg">
      <g id="clickedges">
        <path
          class="edges"
          v-for="item in edge_data.edges"
          :key="item.edge"
          :d="item.d"
          @click="edgeClicked(item.edge)"
        />
      </g>
    </svg>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "EdgeSVG",
  data() {
    return {
      edge_data: "",
      output_svg: ""
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/get_edges")
      .then(response => (this.edge_data = response.data));
  },
  methods: {
    edgeClicked: function(edge) {
      axios
        .get("http://localhost:5000/edge_click?edge=" + edge)
        .then(response => this.$emit("outsvg", response.data));
    }
  }
};
</script>

<style>
.edge-model {
  grid-column: 1 / 4;
  grid-row: 1;
  display: grid;
  align-items: center;
  z-index: 10;
}

.edges:hover {
  opacity: 1;
}
.edges {
  opacity: 0;
  stroke: #ec008c;
  stroke-width: 3px;
}
</style>
