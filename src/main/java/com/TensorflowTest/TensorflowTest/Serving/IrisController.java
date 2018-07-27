package com.TensorflowTest.TensorflowTest.Serving;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class IrisController {

    @Autowired
    IrisClassifierService irisClassifierService;

    @GetMapping(value = "/iris/classify/class")
    public Iris.IrisType classify(Iris iris) {
        return irisClassifierService.classify(iris);
    }

    @GetMapping(value = "/iris/classify/probabilities")
    public Map<Iris.IrisType, Float> classificationProbabilities(Iris iris) {
        return irisClassifierService.classificationProbabilities(iris);
    }

}