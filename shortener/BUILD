load(
  "@io_bazel_rules_python//python:python.bzl",
  "py_binary", "py_library", "py_test"
)

load("@requirements//:requirements.bzl", "all_requirements")

py_binary(
  name = "shortner",
  srcs = ["shortner.py"],
  data = glob(["templates/*"]),
  deps = ["//lib:data"] + all_requirements
)
