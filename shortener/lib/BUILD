load(
  "@io_bazel_rules_python//python:python.bzl",
  "py_binary", "py_library", "py_test"
)

load("@test_requirements//:requirements.bzl", all_test_requirements="all_requirements")

package(default_visibility=["//visibility:public"])

py_library(
  name = "data",
  srcs = ["data.py"],
)
  
py_test(
  name = "data_test",
  srcs = ["data_test.py"],
  deps = all_test_requirements
)
