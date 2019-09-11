window.onload = function() {
  // Get the full redirect URL with URL Fragments.
  var redirect_url = String(window.location);
  // Display the full redirect URL.
  document.getElementsByName("redirect_url")[0].value = redirect_url;

  // Swap the # for ? to make the URL look like it has query parameters, not fragments.
  var redirect_url_altered = redirect_url.replace("#", "?");

  // Parse altered url for parameters.
  const url = new URL(redirect_url_altered);

  // Update the input fields with values from query parameters.
  const input_names = ["access_token", "expires_in", "token_type", "scope", "state"];
  for (input_name of input_names) {
    document.getElementsByName(input_name)[0].value = String(url.searchParams.get(input_name));
  }
};
