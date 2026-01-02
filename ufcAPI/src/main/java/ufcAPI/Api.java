package ufcAPI;
import com.google.gson.Gson;
import static spark.Spark.*;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;
import java.util.stream.Collectors;

public class Api {
    public static void main(String[] args) throws Exception{
        port(8080);

        get("/", (req, res) -> {
            return "External API access to models";
        });

        post("/predict", (req, res) -> {
            Gson gson = new Gson();
            DetailPackage data = gson.fromJson(req.body(), DetailPackage.class);
            String prediction = outcomePrediction(data);
            return prediction;
        });

        get("/classify", (req, res) -> {
            String fighterName = req.queryParams("fighterName");
            float SLpM = Float.parseFloat(req.queryParams("SLpM"));
            float Str_Acc = Float.parseFloat(req.queryParams("Str_Acc"));
            float SApM = Float.parseFloat(req.queryParams("SApM"));
            float TD_Acc = Float.parseFloat(req.queryParams("TD_Acc"));
            float TD_Def = Float.parseFloat(req.queryParams("TD_Def"));
            
            HashMap<String, Object> data = new HashMap<>();
            data.put("fighterName", fighterName);
            data.put("SLpM", SLpM);
            data.put("Str_Acc", Str_Acc);
            data.put("SApM", SApM);
            data.put("TD_Acc", TD_Acc);
            data.put("TD_Def", TD_Def);
            
            String classification = fighterClassification(data);
            return classification;
        });

        get("/percentageStriker", (req, res) -> {
            String fighterName = req.queryParams("fighterName");
            float SLpM = Float.parseFloat(req.queryParams("SLpM"));
            float Str_Acc = Float.parseFloat(req.queryParams("Str_Acc"));
            float SApM = Float.parseFloat(req.queryParams("SApM"));
            float TD_Acc = Float.parseFloat(req.queryParams("TD_Acc"));
            float TD_Def = Float.parseFloat(req.queryParams("TD_Def"));
            
            HashMap<String, Object> data = new HashMap<>();
            data.put("fighterName", fighterName);
            data.put("SLpM", SLpM);
            data.put("Str_Acc", Str_Acc);
            data.put("SApM", SApM);
            data.put("TD_Acc", TD_Acc);
            data.put("TD_Def", TD_Def);
            String result = percentageStriker(data);
            return result;
        });


        /* 
        double[] stats = {1,25,8,30,2,40,0,10,5,3,15,6,4,55,20,10,60,5,8};
        DetailPackage p = new DetailPackage("Mark Smith", stats, "f1", "f2");

        String output = outcomePrediction(p);
        System.out.print(output); */
    }

    public static String fighterClassification(Map<String, Object> data) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        String url = "http://127.0.0.1:8000/classifyFighter?fighterName=" + URLEncoder.encode(data.get("fighterName").toString(), StandardCharsets.UTF_8) +
                "&SLpM=" + data.get("SLpM") +
                "&Str_Acc=" + data.get("Str_Acc") +
                "&SApM=" + data.get("SApM") +
                "&TD_Acc=" + data.get("TD_Acc") +
                "&TD_Def=" + data.get("TD_Def");
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String outcomePrediction(DetailPackage p) throws Exception{ 
        HttpClient client = HttpClient.newHttpClient();
        //works fine as basic example now implement the api version
        // Using classic string concatenation instead of Java 15+ text blocks for compatibility

        String featuresJson = Arrays.stream(p.getStats())
            .mapToObj(Double::toString)
            .collect(Collectors.joining(", ", "[", "]"));
            
        String jsonBody = "{ " +
            "\"fighter1Name\": \"" + p.getFighter1() + "\", " +
            "\"fighter2Name\": \"" + p.getFighter2() + "\", " +
            "\"ref\": \"" + p.getRef() + "\", " +
            "\"features\": " + featuresJson +
            "}";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/predictOutcome"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response =
                client.send(request, HttpResponse.BodyHandlers.ofString());

        if(response.statusCode() != 200) {
            throw new Exception("Request Failed");
        }

        return response.body();
    }

    public static String percentageStriker(Map<String, Object> data) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        String url = "http://127.0.0.1:8000/fighterStylePercentage?fighterName=" + URLEncoder.encode(data.get("fighterName").toString(), StandardCharsets.UTF_8) +
                "&SLpM=" + data.get("SLpM") +
                "&Str_Acc=" + data.get("Str_Acc") +
                "&SApM=" + data.get("SApM") +
                "&TD_Acc=" + data.get("TD_Acc") +
                "&TD_Def=" + data.get("TD_Def");
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}

