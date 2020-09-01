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
    getOtherEdge: function (edge) {
      const joints = Object.assign({}, this.joints);
      const edge_path = edge.getAttribute("d");
      for (const joint in joints) {
        if (joints[joint].edge_a.d === edge_path) {
          const otheredge = document.getElementById(
            "edge" + joints[joint].edge_b.edge
          );
          return otheredge;
        }
        if (joints[joint].edge_b.d === edge_path) {
          const otheredge = document.getElementById(
            "edge" + joints[joint].edge_a.edge
          );
          return otheredge;
        }
      }
      return false;
    },
    edgeHover: function (event) {
      const edge = event.target;
      this.highlightEdge(edge);
      const otherEdge = this.getOtherEdge(edge);
      if (otherEdge) {
        console.log("found the joint", otherEdge);
        this.highlightEdge(otherEdge);
      }
    },
    edgeUnhover: function (event) {
      const edge = event.target;
      this.unhighlightEdge(edge);
      const otherEdge = this.getOtherEdge(edge);
      if (otherEdge) {
        console.log("found the joint", otherEdge);
        this.unhighlightEdge(otherEdge);
      }
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
