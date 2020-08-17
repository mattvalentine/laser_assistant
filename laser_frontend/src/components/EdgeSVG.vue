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
        />
      </g>
    </svg>
  </div>
</template>

<script>
export default {
  name: "EdgeSVG",
  props: ["edge_data"],
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
  },
};
</script>

<style>
.edge-layer {
  z-index: 10;
}

.edges:hover {
  opacity: 0.75;
}

.edges {
  opacity: 0;
  stroke: #ec008c;
  stroke-width: 3px;
}

.activeedge {
  opacity: 1;
}
</style>
