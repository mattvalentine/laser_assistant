<template>
  <div class="edge-layer model">
    <svg id="Layer" :viewBox="edge_data.viewBox" xmlns="http://www.w3.org/2000/svg">
      <g id="clickedges">
        <path
          class="edges"
          :id="'edge'+item.edge"
          v-for="item in edge_data.edges"
          :key="item.edge"
          :d="item.d"
          @click="edgeClicked(item)"
          @mouseover="edgeHover"
          @mouseleave="edgeUnhover"
        />
      </g>
    </svg>
  </div>
</template>

<script>
export default {
  name: "EdgeSVG",
  props: ["edge_data", "joints"],
  data() {
    return {
      output_svg: "",
    };
  },

  methods: {
    edgeClicked: function (edge) {
      // console.log(edge);

      this.$emit("edgeClick", edge);
    },
    find_joint_from_edge: function (edge) {
      console.log(edge);
      return "Joint1";
    },
    edgeHover: function (event) {
      const edge = event.target;
      const classnames = edge.className.baseVal;
      this.highlightEdge(edge);
      if (classnames.indexOf("joint") >= 0) {
        console.log("joint");
        console.log(this.joints);
        this.find_joint_from_edge(edge);
      }
    },
    edgeUnhover: function (event) {
      const edge = event.target;
      this.unhighlightEdge(edge);
    },
    highlightEdge: function (edge) {
      const classnames = edge.className.baseVal;
      if (classnames.indexOf("active") >= 0) return;
      if (classnames.indexOf("hover") >= 0) return;
      edge.className.baseVal = classnames + " hovered";
    },
    unhighlightEdge: function (edge) {
      const classnames = edge.className.baseVal;
      edge.className.baseVal = classnames.replace(/ hovered/g, "");
    },
  },
};
</script>

<style>
.edge-layer {
  z-index: 10;
}

.edges {
  opacity: 0;
  stroke: #ec008c;
  stroke-width: 3px;
}

/* .edges:hover, */
.hovered {
  opacity: 0.75;
}

.activeedge {
  opacity: 1;
}
</style>
