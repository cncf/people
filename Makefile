validate:
	docker run --rm -e GITHUB_WORKSPACE="." -e INPUT_SCHEMA="/data/schema.json" -e INPUT_JSONS="/data/people.json" -v $$(pwd):/service/data orrosenblatt/validate-json-action:latest