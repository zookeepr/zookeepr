<div style="padding: 0.5em">
<script charset="utf-8" src="http://widgets.twimg.com/j/2/widget.js"></script>
<script>
new TWTR.Widget({
  version: 2,
  type: 'search',
  search: '#pycon-au',
  interval: 30000,
  title: '',
  subject: '#pycon-au',
  width: 'auto',
  height: 300,
  theme: {
    shell: {
      background: '#3d91d6',
      color: '#ffffff'
    },
    tweets: {
      background: '#ffffff',
      color: '#444444',
      links: '#03008F'
    }
  },
  features: {
    scrollbar: true,
    loop: true,
    live: true,
    behavior: 'default'
  }
}).render().start();
</script></div>
