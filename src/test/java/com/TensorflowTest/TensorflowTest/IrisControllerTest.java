/*package com.TensorflowTest.TensorflowTest;

import com.TensorflowTest.TensorflowTest.Serving.Iris;
import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import org.junit.Test;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.web.servlet.MvcResult;

import java.io.UnsupportedEncodingException;
import java.util.Locale;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class IrisControllerTest extends BaseControllerTest {

    @Test
    public void classify() throws Exception {

        String urlTemplate = "/iris/classify/class?petalLength=%.1f&petalWidth=%.1f&sepalLength=%.1f&sepalWidth=%.1f";

        // Locale.US to make sure the numbers are with period instead of comma.
        String urlRequest = String.format(Locale.US, urlTemplate,1.3f, 0.3f,5.0f, 3.5f);
        MvcResult mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertEquals(Iris.IrisType.SETOSA.toString(), mvcResult.getResponse().getContentAsString().replace("\"",""));

        urlRequest = String.format(Locale.US, urlTemplate,4.4f, 1.4f, 6.7f, 3.1f);
        mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertEquals(Iris.IrisType.VERSICOLOUR.toString(), mvcResult.getResponse().getContentAsString().replace("\"",""));

        urlRequest = String.format(Locale.US, urlTemplate,6.1f, 1.9f,7.4f, 2.8f);
        mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertEquals(Iris.IrisType.VIRGINICA.toString(), mvcResult.getResponse().getContentAsString().replace("\"",""));
    }

    @Test
    public void classificationProbabilities() throws Exception {

        String urlTemplate = "/iris/classify/probabilities?petalLength=%.1f&petalWidth=%.1f&sepalLength=%.1f&sepalWidth=%.1f";

        // Locale.US to make sure the numbers are with period instead of comma.
        String urlRequest = String.format(Locale.US, urlTemplate, 1.3f, 0.3f, 5.0f, 3.5f);
        MvcResult mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertProbabilitiesResponse(mvcResult.getResponse(), Iris.IrisType.SETOSA);

        urlRequest = String.format(Locale.US, urlTemplate, 4.4f, 1.4f, 6.7f, 3.1f);
        mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertProbabilitiesResponse(mvcResult.getResponse(), Iris.IrisType.VERSICOLOUR);

        urlRequest = String.format(Locale.US, urlTemplate, 6.1f, 1.9f, 7.4f, 2.8f);
        mvcResult = this.mockMvc.perform(get(urlRequest))
                .andExpect(status().isOk()).andReturn();

        assertProbabilitiesResponse(mvcResult.getResponse(), Iris.IrisType.VIRGINICA);
    }

    private void assertProbabilitiesResponse(MockHttpServletResponse mockHttpServletResponse, Iris.IrisType expectedType) throws UnsupportedEncodingException {
        // Extract the probabilities response
        Gson gson = new Gson();
        LinkedTreeMap<String, Float> probabilities;
        probabilities = (LinkedTreeMap<String, Float>) gson.fromJson(mockHttpServletResponse.getContentAsString(), Map.class);
        // Assert
        assertEquals(expectedType.toString(), getPredictedType(probabilities));
        assertProbabilities(probabilities);
    }

    private String getPredictedType(LinkedTreeMap<String, Float> probabilities) {
        // The predicted type is the one with the highest probabilities
        String predictedType = probabilities.entrySet().stream().max(Map.Entry.comparingByValue()).get().getKey();
        return predictedType;
    }

    private void assertProbabilities(LinkedTreeMap<String, Float> probabilities) {
        // The same amount of entries in the map as the possible values
        assertEquals(probabilities.size(), Iris.IrisType.values().length);

        // All the types have a probability value
        for(Iris.IrisType irisType: Iris.IrisType.values()){
            assertTrue(probabilities.containsKey(irisType.toString()));
        }

        // All the entries have a value
        probabilities.entrySet().stream().forEach(probabilityEntry -> {
            assertTrue(probabilityEntry.getKey() != null);
            assertTrue(probabilityEntry.getValue() != null);
        });
    }
}
*/