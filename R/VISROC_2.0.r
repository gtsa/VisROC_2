if (!"devtools" %in% rownames(installed.packages())) install.packages("devtools")
library(devtools)
if (packageVersion("shiny")<'1.7.1') install_version("shiny", version = "1.7.1", "1")
if (packageVersion("shinyjs")<'2.1') install_version("shinyjs", version = "2.1", "1")
if (packageVersion("shinyBS")<'0.61') install_version("shinyBS", version = "0.61", "1")
if (packageVersion("ggplot2")<'3.3.5') install_version("ggplot2", version = "3.3.5", "1")
if (packageVersion("here")<'1.0.1') install_version("here", version = "1.0.1", "1")
library(shiny)
library(shinyjs)
library(shinyBS)
library(ggplot2)
library(here)


# Define server function
server <- function(input, output, session){
  
  output$tb1 <- renderUI({
    tags$img(src='graph_interpretation.svg', style="max-width: 100%; max-height: 100%; height: inherit; position:relative; bottom:-30px;")
  })
  
  output$tb2 <- renderUI({
    tags$img(src='graph_interpretation.svg', style="max-width: 100%; max-height: 100%; height: inherit; position:relative; bottom:-30px")
  })
  
  values <- reactiveValues(data_valid = 0, actions_sequence=c(""), file_to_use_exist = 0, file_diktis=0 )
  
  observeEvent(input$file_browser, {
    inFile <- input$file_browser$datapath
    values$actions_sequence <- append(values$actions_sequence, "File")
    values$file_to_use_exist <- 1
    
  })
  
  observeEvent(input$reset, {
    inFile <- NULL
    reset('file_browser')
    values$actions_sequence <- append(values$actions_sequence, "Reset")
    values$file_to_use_exist <- 0
  })
  
  observe(if (values$file_to_use_exist == 0) values$file_diktis <- 0 else values$file_diktis <- 1)
  
  observeEvent(input$submit, {
    
    style <- "old"
    # style <- isolate(input$style)
    
    withProgress(message = 'Calculation in Progress', detail = "0 %", style = style, value = 0, {
      prog_decimal_precision <- c(0,1) #c(for N<400, for N>=400)
      setProgress(value=0)
      #Sys.sleep(.00001)
      #prog <- prog + 1
      # Update progress

    
    if ((is.null(input$file_browser)&(values$actions_sequence[length(values$actions_sequence)]!="Reset"))) {
      inFile <- NULL
      values$file_to_use_exist <- 0
    } else {
      if (max(c(0,which(values$actions_sequence == "Reset")))>=max(c(0,which(values$actions_sequence == "File")))){
        inFile <- NULL
        values$file_to_use_exist <- 0
      } else {
        inFile <- input$file_browser$datapath
        values$file_to_use_exist <- 1
      }
    }
    values$actions_sequence <- append(values$actions_sequence, "Submit")
    
    #clear text output
    output$text1 <- renderText(" ")
    output$text2 <- renderText(" ")
    output$text3 <- renderText(" ")
    output$text4 <- renderText(" ")
    output$text5 <- renderText(" ")
    output$text6 <- renderText(" ")
    output$text7 <- renderText(" ")
    output$text8 <- renderText(" ")
    output$text9 <- renderText(" ")
    output$text10 <- renderText(" ")
    output$text11 <- renderText(" ")
    output$text12 <- renderText(" ")
    output$text13 <- renderText(" ")
    output$text14 <- renderText(" ")
    
    
    ROCti <- input$title
    p    <-  input$p
    q    <-  input$q
    N    <-  input$N
    uauc <-  input$uauc
    f1   <-  input$f1
    h1   <-  input$h1
    ifault <- 0
    

    
    # Calculate the steps of the process so as to initialise progressbar
    steps_calc <- (N+1)*(N+1)+2002
    if (N>=400) prog_decimal_precision <- prog_decimal_precision[2] else prog_decimal_precision <- prog_decimal_precision[1]
    #progress_bar = ttk.Progressbar(status, length=1015, mode="determinate", maximum=steps_calc, value=0)
    #progress_bar.grid(row=0, column=0)
    
    if (! is.null(inFile)){
      if (tolower(tools::file_ext(inFile)) == "csv") {
        ROCinFile <- read.csv(inFile,
                              header=FALSE,
                              sep = ",")
      } else {
        ROCinFile <- read.csv(inFile,
                              header=FALSE,
                              sep = "")
      }
      ROCinFile[] <- suppressWarnings(lapply(ROCinFile, function(x) as.numeric(gsub(",",".",x))))
      zero0 <- c(0, 0)
      ROCinFile <- rbind(zero0, ROCinFile)
      
      area <- 0.0
      xold_area <- 0.0
      yold_area <- 0.0
      Area_input <- ROCinFile
      unity <- c(1,1)
      Area_input <- rbind(Area_input, unity)
      if (any(is.na(Area_input))==FALSE) {
        if (sum(Area_input[1,]!=Area_input[2,])==0){Area_input <- Area_input[-1,]}
        if (sum(Area_input[nrow(Area_input),]!=Area_input[nrow(Area_input)-1,])==0){Area_input <- Area_input[-nrow(Area_input),]}
      }
      nlines <- nrow(Area_input)
      for (line in 1:nlines) {
        x_area=Area_input[[c(line),c(1)]]
        y_area=Area_input[[c(line),c(2)]]
        area=area+(y_area+yold_area)*(x_area-xold_area)/2.0
        xold_area=x_area
        yold_area=y_area
      }
      #uauc <- area
      names(ROCinFile) <- c("x", "y")
      if (exists("Area_input")) { if ((ncol(Area_input) != 2) | (any(is.na(Area_input))==TRUE)) 
      {ifault <- max(ifault,1)
      values$data_valid <-1
      } else {
        ifault <- 0
        values$data_valid <- 0}}
    } else {
      values$data_valid <- 0
    }
    
    
    
    #initialise 'freq', 'work', 'cdf', 'pdf', 'auc1', 'auccr', 'kcr', 'val'
    freq  <- 0
    work  <- 0
    cdf   <- 0
    pdf   <- 0
    auc1  <- 0
    auccr <- 0
    kcr   <- 0
    val   <- 0
    
    mm <- 1
    message1 <- NULL
    message2 <- NULL
    message3 <- NULL
    message4 <- NULL
    message5 <- NULL
    message6 <- NULL
    message7 <- NULL  
    
    # Check the validity of input parameters
    if ((is.numeric(p) == FALSE) | (is.numeric(p) == TRUE && ( p%%1 != 0 | p <= 0 ))) {ifault <- 2}
    if ((is.numeric(q) == FALSE) | (is.numeric(q) == TRUE && ( q%%1 != 0 | q <= 0 ))) {ifault <- 2}
    if (is.numeric(uauc) == TRUE & uauc < 0.5 & uauc  > 0 ) {uauc <- 0.51; ifault <- max(ifault,1)}
    if ((is.numeric(uauc) == FALSE) | (is.numeric(uauc) == TRUE & uauc  <= 0 | uauc > 1 )) {ifault <- 2}
    if (is.numeric(f1) == FALSE) {ifault <- 2}
    if (is.numeric(f1) == TRUE && ( f1 > 1 | f1 < 0 )) {f1 <- 0.65; ifault <- max(ifault,1)}
    if (is.numeric(h1) == FALSE) {ifault <- 2}
    if (is.numeric(h1) == TRUE && ( h1 > 1 | h1 < 0 )) {h1 <- 0.75; ifault <- max(ifault,1)}
    if (h1 <= f1) {ifault <- max(ifault,1); mauc <- h1; h1 <- f1; f1 <- mauc}
    if(ifault==2) output$text14 <- renderText("<p style=\'color:red;\'><strong>fault 2</strong>:<br><em>Illegal input values.<br>Calculations and plots are not possible</em></p>")
    req(ifault<2)
    #Check on the use of the Gaussian approximation
    case <- 0
    if ((max(p,q) >= 30) && (p + q >= 40)) {case <- 1}
    if (case == 0) {
      #Use of AS62 to estimate the distribution of AUC
      piqo <- min(p,q)
      pq1 <- p*q+1
      paxo <- max(p,q)
      q1 <- paxo+1	
      
      for(i in 1:q1) {
        freq[i] <- 1
      }
      q1 <- q1+1
      if (pq1 >= q1) {
        for(i in q1:pq1) {
          freq[i]=0
        }
      }
      
      work[1] <- 0
      iq <- paxo
      if (piqo >= 2) {
        for(i in 2:piqo) {
          work[i] <- 0
          iq <- iq+paxo
          q1 <- iq+2
          l  <-1+iq/2
          w  <- i
          for(j in 1:l) {
            w  <- w+1
            q1 <- q1-1
            sumAS62=freq[j]+work[j]
            freq[j]=sumAS62
            work[w]=sumAS62-freq[q1]
            freq[q1]=sumAS62
          }
        }
      }
      
      sumAS62 <- 0
      for(i in 1:(p*q+1)) {
        sumAS62 <- sumAS62+freq[i]
        auc1[i] <- 1.0-(i-1.0)/(p*q)
      }
      
      cdf[1] <- 1.0
      for(i in 1:(p*q+1)) {
        pdf[i]   <- freq[i]/sumAS62
        auc1[i]  <- 1.0-(i-1.0)/(p*q)
        cdf[i+1] <- cdf[i]-pdf[i]
        if (cdf[i] >= 0.90) {auccr[1] <- auc1[i]}
        if (cdf[i] >= 0.95) {auccr[2] <- auc1[i]}
        if (cdf[i] >= 0.99) {auccr[3] <- auc1[i]} 
      }	    
    }
    #Use of Gaussian approximation
    if (case == 1) {
      s=sqrt(1.0/q+1.0/p+1.0/(p*q))/sqrt(12.0)
      auccr[1]=0.50+1.2816*s
      auccr[2]=0.50+1.6449*s
      auccr[3] = min(0.50 + 2.3264 * s, 0.999999999999999)
    }

    #Calculate k-values for three AUC confidence levels
    for(l in 1:3) {
      y0    <- auccr[l]
      know  <- 0
      flag1 <- 0
      while (flag1 == 0) {
        k      <- know
        x1     <- (p*q-sqrt(p**2*q**2+q*(p+k)*(k*k+q*(k-p))))/(2.0*q*(p+k))+0.5
        r      <- sqrt(k+4.0*q*(x1-x1*x1))
        r0     <- sqrt(k)
        auc    <- 1.0-x1/2.0+(q/(q+k))*(x1-1.0)*x1/2.0+sqrt(k*(k+q+p)/p)/(2.0*(k+q))*((k+q)*atan(sqrt(q)*(2.0*x1-1.0)/r)/(4.0*sqrt(q))+(2.0*x1-1.0)*r/4.0+(k+q)*atan(sqrt(q)/r0)/(4.0*sqrt(q))+r0/4.0)
        kold   <- know
        x1old  <- x1
        aucold <- auc
        k      <- kold+0.001
        x1     <- (p*q-sqrt(p**2*q**2+q*(p+k)*(k*k+q*(k-p))))/(2.0*q*(p+k))+0.5
        r      <- sqrt(k+4.0*q*(x1-x1*x1))
        r0     <- sqrt(k)
        auc    <- 1.0-x1/2.0+(q/(q+k))*(x1-1.0)*x1/2.0+sqrt(k*(k+q+p)/p)/(2.0*(k+q))*((k+q)*atan(sqrt(q)*(2.0*x1-1.0)/r)/(4.0*sqrt(q))+(2.0*x1-1.0)*r/4.0+(k+q)*atan(sqrt(q)/r0)/(4.0*sqrt(q))+r0/4.0)
        dauc <- (auc-aucold)/0.001
        know <- kold-(aucold-y0)/dauc
        if (abs(know-kold) <= 0.001*kold) {flag1 <- 1}
        
      }
      kcr[l] <- know
    }
    
    out_CL_data <- data.frame(x1=double(),y1=double(),y2=double(),y3=double())
    

      prog <- 0
      for (ix in 0:1000) {
        x <- ix/1000.0
        for (l in 1:3) {
          k    <- kcr[l]
          valy <- 0.5+q/(q+k)*(x-0.5)+0.5/(k+q)*sqrt(k*(k+q+p)*(k+4.0*q*(x-x*x))/p)
          val[l]=valy	
        }
        New_out_CL_data <- c(x, val[1], val[2], val[3])
        out_CL_data <- rbind(out_CL_data, New_out_CL_data) 
        # Long Running Task
        prog <- prog + 1
        # Update progress
        incProgress(1/steps_calc, detail = (paste("(",format(round(100*prog/steps_calc,prog_decimal_precision),
                                                              nsmall = prog_decimal_precision),") %")))
        Sys.sleep(.003)
      }
      
      names(out_CL_data) <- c("x1", "y1", "y2", "y3")
      
      
      #Calculation of the p field on the ROC diagram
      out_field <- data.frame(x=double(),y=double(),z=double())
      x <- 0.0
      y <- 0.0
      erf <- function(x) 2 * pnorm(x * sqrt(2)) - 1
      
      setProgress(value = 1001/steps_calc)
      
      for (ix in 0:N) {
        for (iy in 0:N) {
          x      <- ix/N
          y      <- iy/N
          xv     <- x-0.5
          yv     <- y-0.5
          k      <- 2*(p*yv**2+q*xv**2)-0.5*(p+q)+sqrt((2*(p*yv**2+q*xv**2)-0.5*(p+q))**2+4*p*q*(xv-yv)**2)
          x1     <- (p*q-sqrt(p**2*q**2+q*(p+k)*(k*k+q*(k-p))))/(2.0*q*(p+k))+0.5
          r      <- sqrt(k+4.0*q*(x1-x1*x1))
          r0     <- sqrt(k)
          auc    <- 1.0-x1/2.0+(q/(q+k))*(x1-1.0)*x1/2.0+sqrt(k*(k+q+p)/p)/(2.0*(k+q))*((k+q)*atan(sqrt(q)*(2.0*x1-1.0)/r)/(4.0*sqrt(q))+(2.0*x1-1.0)*r/4.0+(k+q)*atan(sqrt(q)/r0)/(4.0*sqrt(q))+r0/4.0)
          if (case == 1) {
            valy <- (erf((auc-0.50)/sqrt(2.0)/s)+1.0)/2.0
          }
          if (case == 0) {
            valy <- cdf[1]
            for (i in 2:(p*q+1)) {
              if (auc1[i] >= auc) {
                valy <- cdf[i]
              }
            }
          }
          New_out_field <- c(x, y, 1-valy)
          out_field <- rbind(out_field, New_out_field)
        }
        prog <- prog + N + 1
        # Long Running Task
        #Sys.sleep(.25)
        # Update progress
        incProgress((N+1)/steps_calc, detail = (paste("(", format(round(100*prog/steps_calc, prog_decimal_precision),
                                                                  nsmall = prog_decimal_precision),") %")))
        #Sys.sleep(.00001)
      }
      
      names(out_field) <- c("x", "y", "z")
      
      #Calculation of the p value for the user defined uauc
      out_p_data <- data.frame(a1=double(),a2=double(),a3=double(),a4=double(),a5=double())
      
      auc <- uauc
      if (case == 1) {valy=(erf((auc-0.50)/sqrt(2.0)/s)+1.0)/2.0}
      if (case == 0) {
        valy=cdf[1]
        for (i in 2:(p*q+1)) {
          if (auc1[i] >= auc) {
            valy=cdf[i]
          }
        }
      }
      out_p_data <- c(1.0-valy, uauc, p, q, ifault)
      names(out_p_data) <- c("p_Value", "UserDefAUC", "p", "q", "ifault")
      PVAUC <- 1-valy
      
      
      #Calculation of the p value for the file of user's ROC data
      if (! is.null(inFile))
      {
        out_p_data_file <- data.frame(a1=double(),a2=double(),a3=double(),a4=double(),a5=double())
        
        auc_file <- area
        if (case == 1) {valy_file=(erf((auc_file-0.50)/sqrt(2.0)/s)+1.0)/2.0}
        if (case == 0) {
          valy_file=cdf[1]
          for (i in 2:(p*q+1)) {
            if (auc1[i] >= auc_file) {
              valy_file=cdf[i]
            }
          }
        }
        out_p_data_file <- c(1.0-valy_file, area, p, q, ifault)
        names(out_p_data_file) <- c("p_Value", "UserFileAUC", "p", "q", "ifault")
        PVAUC_file <- 1-valy_file
      }
      
      
      #Calculation of the p value for the user defined uauc
      out_p_data <- data.frame(a1=double(),a2=double(),a3=double(),a4=double(),a5=double())
      
      auc <- uauc
      if (case == 1) {valy=(erf((auc-0.50)/sqrt(2.0)/s)+1.0)/2.0}
      if (case == 0) {
        valy=cdf[1]
        for (i in 2:(p*q+1)) {
          if (auc1[i] >= auc) {
            valy=cdf[i]
          }
        }
      }
      out_p_data <- c(1.0-valy, uauc, p, q, ifault)
      names(out_p_data) <- c("p_Value", "UserDefAUC", "p", "q", "ifault")
      PVAUC <- 1-valy
      
      
      
      #Calculations based on the k-ellipse passing through h1,f1
      out_F1H1 <- data.frame(a1=double(),a2=double(),a3=double(),a4=double(),a5=double(),a6=double(),a7=double())
      x   <- f1
      y   <- h1
      xv  <- x-0.5
      yv  <- y-0.5
      k   <- 2*(p*yv**2+q*xv**2)-0.5*(p+q)+sqrt((2*(p*yv**2+q*xv**2)-0.5*(p+q))**2+4*p*q*(xv-yv)**2)
      x1  <- (p*q-sqrt(p**2*q**2+q*(p+k)*(k*k+q*(k-p))))/(2.0*q*(p+k))+0.5
      r   <- sqrt(k+4.0*q*(x1-x1*x1))
      r0  <- sqrt(k)
      auc <- 1.0-x1/2.0+(q/(q+k))*(x1-1.0)*x1/2.0+sqrt(k*(k+q+p)/p)/(2.0*(k+q))*((k+q)*atan(sqrt(q)*(2.0*x1-1.0)/r)/(4.0*sqrt(q))+(2.0*x1-1.0)*r/4.0+(k+q)*atan(sqrt(q)/r0)/(4.0*sqrt(q))+r0/4.0)
      mauc <- auc
      auc  <- mauc
      
      if (case == 1) {
        valy <- (erf((auc-0.50)/sqrt(2.0)/s)+1.0)/2.0
      }
      if (case == 0) {
        valy <- cdf[1]
        for (i in 2:(p*q+1)) {
          if (auc1[i] >= auc) {
            valy <- cdf[i]
          }
        }
      }
      mval <- valy
      out_F1H1 <- c(1.0-mval, f1, h1, ifault, p, q, mauc)
      names(out_F1H1) <- c("p_Value", "F1", "H1", "ifault", "p", "q", "AUC")
      PVAUCF1H1 <- 1.0-mval
      
      
      setProgress(value = ((N+1)**2+1001)/steps_calc)
      #Export the k-ellipse passing through h1,f1
      out_k_F1H1 <- data.frame(a1=double(),a2=double(),a3=double())
      for (ix in 0:1000) {
        xk <- ix/1000.0
        valyF1H1 <- 0.5+q/(q+k)*(xk-0.5)+0.5/(k+q)*sqrt(k*(k+q+p)*(k+4.0*q*(xk-xk*xk))/p)	
        New_out_k_F1H1 <- c(xk, valyF1H1, k)
        out_k_F1H1 <- rbind(out_k_F1H1, New_out_k_F1H1)
        prog <- prog + 1
        incProgress(1/steps_calc, detail = (paste("(",format(round(100*prog/steps_calc, prog_decimal_precision),
                                                             nsmall = prog_decimal_precision),") %")))
        Sys.sleep(.003)
      }
      names(out_k_F1H1) <- c("x", "y", "k")
      
      
      output$text1 <- renderText(paste("p-value of AUC:",PVAUC))
      output$text2 <- renderText(paste("User defined AUC:",uauc))
      output$text3 <- renderText(paste("P:",p))
      output$text4 <- renderText(paste("Q:",q))
      output$text5 <- renderText(paste("p-value of k-ellipse (F<sub>1</sub>,H<sub>1</sub>):",PVAUCF1H1))
      output$text6 <- renderText(paste("AUC of k-ellipse (F<sub>1</sub>,H<sub>1</sub>):",mauc))
      output$text7 <- renderText(paste("F<sub>1</sub>:",f1))
      output$text8 <- renderText(paste("H<sub>1</sub>:",h1))
      if (! is.null(inFile))
      {
        output$text9 <- renderText(paste("p-value file's ROC data AUC:",PVAUC_file))
        output$text10 <- renderText(paste("File's ROC data AUC:",area))
        output$text11 <- renderText(paste("P:",p))
        output$text12 <- renderText(paste("Q:",q))
      } else {
        output$text13 <- renderText(paste("No input file")) 
      }  
      output$text14 <- renderText({
        if (ifault==0) "No fault"
        else "<p style=\'color:red;\'><strong>fault 1</strong>:<br><em>Illegal input values.<br>Altered values used, as described in the \"Help\" section</em></p>"
      })
      
      
      
      
      
      output$tb1 <-renderUI({
        output$plot1 <- renderPlot({
          if (input$act_view_style == "hit_false")
          {labx="False alarm"
          laby="Hit rate"
          }
          else if (input$act_view_style == "ss")
          {labx="1 - Specificity"
          laby="Sensitivity"
          }
          else {labx="False Positive Rate (FPR)"
          laby="True Positive Rate (TPR)"
          }
          if (! is.null(inFile))
          {
            gp1 <- ggplot() + 
              geom_tile(data=out_field, aes(x, y, fill= z)) + 
              scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
              geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
              geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
              geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
              geom_line(data=ROCinFile, aes(x=x, y=y, colour = "data"), size = 0.8) + 
              geom_point(data=ROCinFile, aes(x=x, y=y), colour = "purple", size = 3) +
              scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red', "data" = 'purple'),
                                 labels = c('10%','5%','1%', "data")) +
              theme(aspect.ratio=1,
                    panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                    panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                    panel.ontop = TRUE,
                    panel.background = element_rect(color = NA, fill = NA),
                    plot.title = element_text(hjust = 0.5)) +
              coord_fixed(ratio = 1) +
              labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
              coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
              guides(color = guide_legend(order = 1), 
                     fill = guide_colourbar(order = 2, barheight = 17)) +
              ggtitle(ROCti)
            
            gp1  
          } else {
            gp1 <- ggplot() + 
              geom_tile(data=out_field, aes(x, y, fill= z)) + 
              scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
              geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
              geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
              geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
              scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red'),
                                 labels = c('10%','5%','1%')) +
              theme(aspect.ratio=1,
                    panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                    panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                    panel.ontop = TRUE,
                    panel.background = element_rect(color = NA, fill = NA),
                    plot.title = element_text(hjust = 0.5)) +
              coord_fixed(ratio = 1) + 
              labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
              coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
              guides(color = guide_legend(order = 1),
                     fill = guide_colourbar(order = 2, barheight = 17)) +
              ggtitle(ROCti)  
            
            gp1
          }
        },
        height = 500, width = 500)
        plotOutput("plot1", height = 500, width = 500)
      })
      
      
      output$tb2 <-renderUI({
        output$plot2 <- renderPlot({
          if (input$act_view_style == "hit_false")
          {labx="False alarm"
          laby="Hit rate"
          }
          else if (input$act_view_style == "ss")
          {labx="1 - Specificity"
          laby="Sensitivity"
          }else {
            labx="False Positive Rate (FPR)"
            laby="True Positive Rate (TPR)"
          }
          gp2 <- ggplot() + 
            geom_tile(data=out_field, aes(x, y, fill= z)) + 
            scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
            geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
            geom_line(data=out_k_F1H1, aes(x=x, y=y, colour = "k-F1_H1"), size = 1, linetype = 'dashed') +
            geom_point(aes(x=f1, y=h1), colour = "purple", size = 4) +
            scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red', "k-F1_H1" = 'purple'),
                               labels = c('10%','5%','1%', bquote("("*F[1]*","*H[1]*")-ellipse"))) +
            theme(aspect.ratio=1,
                  panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.ontop = TRUE,
                  panel.background = element_rect(color = NA, fill = NA),
                  plot.title = element_text(hjust = 0.5)) +
            coord_fixed(ratio = 1) + 
            labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
            coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
            guides(color = guide_legend(order = 1), 
                   fill = guide_colourbar(order = 2, barheight = 17)) +
            ggtitle(ROCti)
          
          gp2
        },
        height = 500, width = 500)
        plotOutput("plot2", height = 500, width = 500)
      })
      
      
      setProgress(value = 1001/steps_calc)
    })
    
    #saving the plots
    
    output$saveData <- downloadHandler(
      filename = function() {
        paste("output", "zip", sep=".")
      },
      content = function(fname) {
        fs <- c()
        tmpdir <- tempdir()
        setwd(tempdir())
        if (input$act_view_style == "hit_false")
        {labx="False alarm"
        laby="Hit rate"
        }
        else if (input$act_view_style == "ss")
        {labx="1 - Specificity"
        laby="Sensitivity"
        }else {
          labx="False Positive Rate (FPR)"
          laby="True Positive Rate (TPR)"
        }
        if (! is.null(inFile))
        {
          ggplot() + 
            geom_tile(data=out_field, aes(x, y, fill= z)) + 
            scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
            geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
            geom_line(data=ROCinFile, aes(x=x, y=y, colour = "data"), size = 0.8) + 
            geom_point(data=ROCinFile, aes(x=x, y=y), colour = "purple", size = 3) +
            scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red', "data" = 'purple'),
                               labels = c('10%','5%','1%', "data")) +
            theme(aspect.ratio=1,
                  panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.ontop = TRUE,
                  panel.background = element_rect(color = NA, fill = NA),
                  plot.title = element_text(hjust = 0.5)) +
            coord_fixed(ratio = 1) + 
            labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
            coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
            guides(color = guide_legend(order = 1), 
                   fill = guide_colourbar(order = 2, barheight = 17)) +
            ggtitle(ROCti)
          ggsave('ROC_plot.pdf')  
        } else {
          ggplot() + 
            geom_tile(data=out_field, aes(x, y, fill= z)) + 
            scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
            geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
            geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
            scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red'),
                               labels = c('10%','5%','1%')) +
            theme(aspect.ratio=1,
                  panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                  panel.ontop = TRUE,
                  panel.background = element_rect(color = NA, fill = NA),
                  plot.title = element_text(hjust = 0.5)) +
            coord_fixed(ratio = 1) +
            labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
            coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
            guides(color = guide_legend(order = 1), 
                   fill = guide_colourbar(order = 2, barheight = 17)) +
            ggtitle(ROCti)  
          
          ggsave('ROC_plot.pdf')
        }
        
        ggplot() + 
          geom_tile(data=out_field, aes(x, y, fill= z)) + 
          scale_fill_gradientn(colours = c("white","#00CC00", "#0080FF"), breaks = (.05*1:10),labels = paste0((5*1:10),"%")) + 
          geom_line(data=out_CL_data, aes(x=x1, y=y1, colour = "10%"), size = 0.8) + 
          geom_line(data=out_CL_data, aes(x=x1, y=y2, colour = "5%"), size = 0.8) +
          geom_line(data=out_CL_data, aes(x=x1, y=y3, colour = "1%"), size = 0.8) + 
          geom_line(data=out_k_F1H1, aes(x=x, y=y, colour = "k-F1_H1"), size = 1, linetype = 'dashed') +
          geom_point(aes(x=f1, y=h1), colour = "purple", size = 4) +
          scale_color_manual(values = c('10%' = '#0080FF','5%' = 'green3','1%' = 'red', "k-F1_H1" = 'purple'),
                             labels = c('10%','5%','1%', bquote("("*F[1]*","*H[1]*")-ellipse"))) +
          theme(aspect.ratio=1,
                panel.grid.major = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                panel.grid.minor = element_line(size = 0.25, linetype = 'dashed',colour = "black"),
                panel.ontop = TRUE,
                panel.background = element_rect(color = NA, fill = NA),
                plot.title = element_text(hjust = 0.5)) +
          coord_fixed(ratio = 1) +
          labs(x = labx, y = laby, fill = "p-value\n", col="k-ellipses           ") +
          coord_cartesian(ylim = c(0.045, 0.955), xlim = c(0.045, 0.955)) +
          guides(color = guide_legend(order = 1),
                 fill = guide_colourbar(order = 2, barheight = 17)) +
          ggtitle(ROCti)
        
        ggsave('F1H1_plot.pdf') 
        
        #Write Files: 'out_field.csv', 'out_p.csv', 'out_CL.csv', 'out_F1H1.csv', 'out_k_F1H1.csv'
        write.table(format(out_field, digits=15), file = "out_field.csv", row.names = FALSE, sep=", ", quote=FALSE, na = "NA")
        write.table(t(format(out_p_data, digits=15)), file = "out_p.csv", row.names = FALSE, sep=", ", quote=FALSE, na = "NA")
        write.table(format(out_CL_data, digits=15), file = "out_CL.csv", row.names = FALSE, sep=", ", quote=FALSE, na = "NA")
        write.table(t(format(out_F1H1, digits=15)), file = "out_F1H1.csv", row.names = FALSE, sep=", ", quote=FALSE, na = "NA")
        write.table(format(out_k_F1H1, digits=15), file = "out_k_F1H1.csv", row.names = FALSE, sep=", ", quote=FALSE, na = "NA")
        fs = c("ROC_plot.pdf", "F1H1_plot.pdf", "out_field.csv","out_p.csv","out_CL.csv","out_F1H1.csv","out_k_F1H1.csv")
        #for (i in c(1,2,3,4,5)) {
        #  path <- paste0("sample_", i, ".csv")
        #  fs <- c(fs, path)
        #  write(i*2, path)
        #}
        zip(zipfile=fname, files=fs)
      },
      contentType = "application/zip"
    )
  })
  output$data_valid <- renderText(values$data_valid)
  outputOptions(output, "data_valid", suspendWhenHidden = FALSE)
  output$file_diktis <- renderText(values$file_diktis)
  outputOptions(output, "file_diktis", suspendWhenHidden = FALSE)
}


# Define UI
ui <- fluidPage(
  useShinyjs(),
  tags$style(".shiny-progress {opacity: 1; background-color:white; height:5px;}"),
  tags$style(".shiny-progress .bar {opacity: 1;}"),
  tags$style(".fa-question-circle {color: dodgerBlue; font-size: 22px; vertical-align:bottom}"),
  tags$style(".fa-info-circle {color: dodgerBlue; font-size: 22px; vertical-align:bottom}"),
  fluidRow( wellPanel(style = "background: dodgerBlue; color: white; font-weight: bold; height:40px; padding:10px" ,"VISROC 2.0")),
  sidebarPanel(width = 4,
               fluidRow(column(6,style='padding:5px;', numericInput(inputId = "p", label = "P", value=15, min = 1)),
                        column(6,style='padding:5px;', numericInput(inputId = "q", label = "Q", value=35, min = 1))), 
               bsTooltip(id = "p", title = "Enter here the number of positive events P"),
               bsTooltip(id = "q", title = "Enter here the number of negative events Q"),
               fluidRow(sliderInput(inputId = "N", label = 'Resolution', min=1, max=1000, value=100 , step=1)),
               bsTooltip(id = "N", title = "Slide to define the resolution, that is the number N of segments in which the interval [0,1] is divided for the calculation of the p-values on a square lattice in the ROC diagram"),
               fluidRow(column(12, style='padding:5px;',div(id='auc_label',numericInput(inputId = "uauc", label = 'User defined AUC', value = 0.51, min = 0.5, max = 1.0, step="any")))),
               tags$style(type="text/css", "#auc_label {color:#00008B}"),
               bsTooltip(id = "uauc", title = "Enter the value of the AUC (Area Under the Curve) of a ROC diagram for which you would like to calculate the p-value"),
               fluidRow(column(6, style='padding:5px;', div(id='f1h1_label', numericInput(inputId = "f1", label = HTML("F<sub>1</sub>"), value=0.65, step=0.01))),
                        column(6, style='padding:5px;', div(id='f1h1_label', numericInput(inputId = "h1", label = HTML("H<sub>1</sub>"), value=0.75, step=0.01)))),
               tags$style(type="text/css", "#f1h1_label {color:#7030A0}"),
               bsTooltip(id = "f1", title = "Enter here the False Positive Rate (False Alarm Rate or 1-Specificity) value F1 of the point (F1,H1) on the ROC diagram through which passes the k-ellipse for which you calculate the p-value. Attention: H1>F1"),
               bsTooltip(id = "h1", title = "Enter here the True Positive Rate (Hit Rate or Sensitivity) value H1 of the point (F1,H1) on the ROC diagram through which passes the k-ellipse for which you calculate the p-value. Attention: H1>F1"), 
               fluidRow(textInput(inputId = "title", label = "Set title:", value = "ROC diagram")),
               bsTooltip(id = "title", title = "Here you can enter the diagram title of your choice"),
               fluidRow(div(id='datafile_label',
                            fileInput(inputId = "file_browser" , label = "Insert file of user's ROC data", multiple = FALSE, accept = c(".csv",".txt"),
                                      width = NULL, buttonLabel = "Browse...", placeholder = "No file selected"),
                            div(style = "margin-top: -40px"),
                            conditionalPanel(id = "Warning_panel", condition = "(output.file_diktis == 1) ", style = "display: none;" ,
                                             column(12, align="right", actionButton('reset', width = '20px', 'x', style = "color: crimson; font-weight: bold; font-size:11px; margin-top:-4px; padding:2px; margin-right: -15px"))))),
               #   fluidRow(textOutput("tbl")),
               div(style = "margin-top: 10px"),
               tags$style(type="text/css", "#datafile_label {color:#00B050}"),
               #   fluidRow(radioButtons(inputId = 'style', label = 'Progress bar style', c('notification', 'old'), inline = TRUE)),
               fluidRow(column(6, align="center", actionButton(inputId = "submit", label = "Submit", style = "background: dodgerBlue; color: white; font-weight: bold")),
                        column(6, align="center", downloadButton("saveData", label = "Save", style = "background: dodgerBlue; color: white; font-weight: bold"))),
               tags$hr(),
               fluidRow(tags$b("Results"), style = "color: dodgerBlue; font-size:16px"),
               tags$br(),
               fluidRow(tags$b("out_p:"), style="color:#00008B"),
               fluidRow(textOutput("text1")),
               fluidRow(textOutput("text2")),
               fluidRow(textOutput("text3")),
               fluidRow(textOutput("text4")),
               tags$br(),
               fluidRow(tags$b("out_F1H1:"), style="color:#7030A0"),
               fluidRow(htmlOutput("text5")),
               fluidRow(htmlOutput("text6")),
               fluidRow(htmlOutput("text7")),
               fluidRow(htmlOutput("text8")),
               tags$br(),
               fluidRow(tags$b("Files_data_ROC:"), style="color:#00B050"),
               fluidRow(textOutput("text9")),
               fluidRow(textOutput("text10")),
               fluidRow(textOutput("text11")),
               fluidRow(textOutput("text12")),
               fluidRow(textOutput("text13")),
               tags$br(),
               fluidRow(htmlOutput("text14"))
               
               
  ),
  
  mainPanel(
    shiny::fluidRow(
      shinydashboard::box(shiny::actionButton(inputId='ab1', label="Help", 
                                              icon = icon("question-circle"), 
                                              onclick ="window.open(href='HelpR.html', '_blank','resizable,height=800,width=640')")
      ), style = "float: right;"
    ),
    
    tabsetPanel(type = "tabs",
                tabPanel("ROC curve",
                         fluidRow(style="height:500px",uiOutput("tb1", align="center")),
                         shiny::actionButton(inputId='graph', label="Graph Interpretation", icon = icon("info-circle"),
                                             onclick ="window.open(href='graph_interpretation.html', '_blank', 'resizable,height=800,width=800')", style = "float: right;"),
                         tags$br(),
                         tags$br(),
                         tags$br(),
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.p <= 0 | Number.isInteger(input.p) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> P must be positive integer" )))),
                         conditionalPanel(id = "Warning_panel", condition = "typeof input.q != 'number' | input.q <= 0 | Number.isInteger(input.q) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> P must be positive integer" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.uauc <= 0 | input.uauc > 1.0 | (!isNaN(parseFloat(input.uauc)) && !isNaN(input.uauc - 0)) == false ", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong>AUC must be a numerical value in the closed interval [0.5, 1]" )))),
                         conditionalPanel(id = "Warning_panel", condition = "input.uauc < 0.5 & input.uauc  > 0" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong>AUC must have a numerical value in the closed interval [0.5, 1].
                                                               <br><em>Value assigned  for calculations and plots: <strong>AUC=0.51</em></strong>" )))),
                         
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.f1 < 0 | input.f1 > 1.0", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> F<sub>1</sub> must have a numerical value in the closed interval [0, 1].
                                                               <br><em>Value assigned for calculations and plots: <strong>F<sub>1</sub>=0.65</em></strong>" )))),
                         conditionalPanel(id = "Warning_panel", condition = "(!isNaN(parseFloat(input.f1)) && !isNaN(input.f1 - 0)) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> F<sub>1</sub> must have a numerical value in the closed interval [0, 1]" )))),
                         
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.h1 == 'number' & (input.h1 < 0 | input.h1 > 1.0)", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> H<sub>1</sub> must have a numerical value in the closed interval [0, 1].
                                                               <br><em>Value assigned for calculations and plots: <strong>H<sub>1</sub>=0.75</em></strong>" )))),
                         conditionalPanel(id = "Warning_panel", condition = "(!isNaN(parseFloat(input.h1)) && !isNaN(input.h1 - 0)) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> H<sub>1</sub> must have a numerical value in the closed interval [0, 1]" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.h1 < input.f1" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px",
                                                             HTML("<strong>Input error:</strong> Value F<sub>1</sub> must be greater than value H<sub>1</sub>. 
                                                               <br><em>New values are assigned: <strong>F<sub>1</sub> = (old H<sub>1</sub>)</strong>, <strong>H<sub>1</sub> = (old F<sub>1</sub>)</em></strong>" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "output.data_valid == 1" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px",
                                                             HTML("<strong>Input error:</strong> user's ROC data is not in two columns or contains NA values.
                                                                  <br><em><strong>Calculations and plots may be misleading</strong></em>" ))))
                ),
                tabPanel("Plot (F1,H1)", 
                         fluidRow(style="height:500px",uiOutput("tb2", align="center")),
                         shiny::actionButton(inputId='graph', label="Graph Interpretation", icon = icon("info-circle"),
                                             onclick ="window.open(href='graph_interpretation.html', '_blank', 'resizable,height=800,width=800')", style = "float: right;"),
                         tags$br(),
                         tags$br(),
                         tags$br(),
                         conditionalPanel(id = "Warning_panel", condition = "input.p <= 0 | Number.isInteger(input.p) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> P must be positive integer" )))),
                         conditionalPanel(id = "Warning_panel", condition = "typeof input.q != 'number' | input.q <= 0 | Number.isInteger(input.q) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> P must be positive integer" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.uauc <= 0 | input.uauc > 1.0 | (!isNaN(parseFloat(input.uauc)) && !isNaN(input.uauc - 0)) == false ", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong>AUC must be a numerical value in the closed interval [0.5, 1]" )))),
                         conditionalPanel(id = "Warning_panel", condition = "input.uauc < 0.5 & input.uauc  > 0" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong>AUC must have a numerical value in the closed interval [0.5, 1].
                                                               <br><em>Value assigned  for calculations and plots: <strong>AUC=0.51</em></strong>" )))),
                         
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.f1 < 0 | input.f1 > 1.0", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> F<sub>1</sub> must have a numerical value in the closed interval [0, 1].
                                                               <br><em>Value assigned for calculations and plots: <strong>F<sub>1</sub>=0.65</em></strong>" )))),
                         conditionalPanel(id = "Warning_panel", condition = "(!isNaN(parseFloat(input.f1)) && !isNaN(input.f1 - 0)) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> F<sub>1</sub> must have a numerical value in the closed interval [0, 1]" )))),
                         
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.h1 == 'number' & (input.h1 < 0 | input.h1 > 1.0)", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> H<sub>1</sub> must have a numerical value in the closed interval [0, 1].
                                                               <br><em>Value assigned for calculations and plots: <strong>H<sub>1</sub>=0.75</em></strong>" )))),
                         conditionalPanel(id = "Warning_panel", condition = "(!isNaN(parseFloat(input.h1)) && !isNaN(input.h1 - 0)) == false", style = "display: none;" ,
                                          fluidRow(wellPanel(style = "background: red; border-color: crimson; border-width: 3px" ,
                                                             HTML("<strong>Input error:</strong> H<sub>1</sub> must have a numerical value in the closed interval [0, 1]" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "input.h1 < input.f1" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px",
                                                             HTML("<strong>Input error:</strong> Value F<sub>1</sub> must be greater than value H<sub>1</sub>. 
                                                               <br><em>New values are assigned: <strong>F<sub>1</sub> = (old H<sub>1</sub>)</strong>, <strong>H<sub>1</sub> = (old F<sub>1</sub>)</em></strong>" )))),
                         
                         conditionalPanel(id = "Warning_panel", condition = "output.data_valid == 1" , style = "display: none;",
                                          fluidRow(wellPanel(style = "border-color: crimson; border-width: 3px",
                                                             HTML("<strong>Input error:</strong> user's ROC data is not in two columns or contains NA values.
                                                                  <br><em><strong>Calculations and plots may be misleading</strong></em>" ))))
                )
    ),
    fluidRow(radioButtons("act_view_style", "View Mode:", c("Hit Rate / False-Alarm Rate" = "hit_false", "Sensitivity / Specificity" = "ss", "True Positive Rate (TPR) / False Positive Rate (FPR)" = "pr"), width = "100%")),
    fluidRow(tags$b("Contact details:"),
             tags$br(),
             ("ac0966@coventry.ac.uk, strichr@phys.uoa.gr,"),
             tags$br(),
             ("georgios.tsagiannis@parisnanterre.fr"), style = "color: dodgerBlue;")                   
    
    #         plotOutput("plotROC")
    
  )
) 


# Create Shiny object
shinyApp(ui = ui, server = server)